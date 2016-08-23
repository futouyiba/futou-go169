from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from go169Message import StoneMessage, ColorSideMessage
from main import get_adjacent_position_set
from game_conf import len_each_side

class Player(ndb.Model):
    """use a player model instead of a score model"""
    # playerID = ndb.IntegerProperty(required=True)
    score = ndb.FloatProperty(default=1000)
    playerName = ndb.StringProperty(required=True)
    wins = ndb.IntegerProperty(default=0)
    loses = ndb.IntegerProperty(default=0)



class GameList(ndb.Model):
    """only store created games that don't have an opponent yet."""
    player_key = ndb.KeyProperty(Player)


class Match(ndb.Model):
    """model representing a Go169 game match."""
    black_player = ndb.KeyProperty(Player, required=False)
    # not required because a match should be joined first.
    white_player = ndb.KeyProperty(Player, required=False)
    # not required because a match should be joined first.
    is_outdated = ndb.BooleanProperty(default=False)
    winner = ndb.KeyProperty(Player, default=None)
    moves = ndb.StringProperty(default="")
    nodes = msgprop.EnumProperty(StoneMessage, repeated=True)

    def __init__(self):
        self.has_eliminated_at_least_one_enemy = False
        self.current_turn_color = ColorSideMessage.black
        # self.moves = []

    # start_playerID is not needed because match always starts with black side.
    def get_player_color(self, player_key):
        if player_key == self.black_player:
            return ColorSideMessage.black
        if player_key == self.white_player:
            return ColorSideMessage.white

    def get_adjacent_friends(self, position):
        this_node = self.get_node_from_position(position)
        wanted_node = this_node
        if this_node == StoneMessage.black_stone_just_put or \
                        this_node == StoneMessage.white_stone_just_put:
            wanted_node = StoneMessage(int(this_node) - 5)
        adjacent_position_set = get_adjacent_position_set(position)
        adjacent_friend_set = set()
        for pos in adjacent_position_set:
            if self.get_node_from_position(pos) == wanted_node:
                adjacent_friend_set.add(pos)
        return adjacent_friend_set

    def get_adjacent_enemies(self, position):
        this_node = self.get_node_from_position(position)
        wanted_node = StoneMessage(3 - int(this_node))
        if this_node == StoneMessage.black_stone_just_put or\
                        this_node == StoneMessage.white_stone_just_put:
            wanted_node = StoneMessage(8 - int(this_node))
        adjacent_position_set = get_adjacent_position_set(position)
        adjacent_enemy_set = set()
        for pos in adjacent_position_set:
            if self.get_node_from_position(pos) == wanted_node:
                adjacent_enemy_set.add(pos)
        return adjacent_enemy_set

    def position_node_has_liberty(self, position):
        adjacent_positions = get_adjacent_position_set(position)
        for pos in adjacent_positions:
            if self.get_node_from_position(pos) == 0:
                return True
        return False

    def get_node_from_position(self, position):
        return self.nodes[position]

    def position_chain_dead(self, position):
        visited, chain = set(), [position]
        while chain:
            focus = chain.pop()
            if focus not in visited:
                if self.position_node_has_liberty(focus):
                    return False
                else:
                    visited.add(focus)
                    chain.extend(self.get_adjacent_friends(focus) - visited)
        return visited

    def make_move(self, position, player_key):
        """change the board status & add a record in board moves."""
        color = self.get_player_color(player_key)
        if not color:
            # send_failure_invalid_player() #todo
            return
        if color != self.current_turn_color:
            # todo send invalid move
            return
        if color == ColorSideMessage.black:
            self.nodes[position] = StoneMessage.black_stone_just_put
        else:
            self.nodes[position] = StoneMessage.white_stone_just_put

        if self.get_node_from_position(position) != StoneMessage.no_stone:
            # send_failure_invalid_move() can use endpoints #todo
            return
        enemies = self.get_adjacent_enemies(position)
        for enemy in enemies:
            if self.nodes[enemy] == StoneMessage.no_stone:
                continue
            dead_enemy_chain = self.position_chain_dead(enemy)
            if dead_enemy_chain:
                # todo not sure there is something to do here
                for chain_component in dead_enemy_chain:
                    self.has_eliminated_at_least_one_enemy = True
                    self.nodes[chain_component] = StoneMessage.no_stone
        if self.has_eliminated_at_least_one_enemy:
            # todo send sucess
            # todo send board nodes
            self.successful_move(position, color)
        else:
            self_dead_chain = self.position_chain_dead(position)
            if self_dead_chain:
                # todo send failure_invalid_move
                self.nodes[position] = StoneMessage.no_stone
                return
            else:
                self.successful_move(position, color)
        self.has_eliminated_at_least_one_enemy = False

    def successful_move(self, position, color):
        self.moves += "%s,%s|" % (position, int(color))
        self.put()
        # todo start counting time (so send mail after 1 hour)

    def initiate_board(self):
        """initiate board. length of each side is defined in game_conf"""
        super.__init__()
        positions = len_each_side * len_each_side
        for i in range(1, positions):
            self.nodes.append(StoneMessage.no_stone)


