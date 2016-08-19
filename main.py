#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import endpoints
from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
import go169Message
from go169Message import StoneMessage
from go169Message import ColorSideMessage
import game_conf
from protorpc import messages
from math import floor


def position_int_to_row_column(integer_postion):
    """takes in a integer postion and returns (row position, column position)
    integratedPosition: a position according to index in the board list"""
    row = floor(integer_postion / game_conf.len_each_side)
    column = integer_postion - row * game_conf.len_each_side
    return row, column


def position_row_column_to_int(row, column):
    """"""
    integer_position = row * game_conf.len_each_side + column
    return integer_position


def get_adjacent_position_set(integrate_position):
    """returns a set including all the adjacent positions, which could be up to 4 positions,
    and down to 2 positions since the board has borders"""
    up = integrate_position - game_conf.len_each_side
    down = integrate_position + game_conf.len_each_side
    left = integrate_position - 1
    right = integrate_position + 1
    adjacent_position_list = [up, down, left, right]
    adjacent_set = set(adjacent_position_list)
    row, column = position_int_to_row_column(integrate_position)
    if row == 0:
        adjacent_set.remove(up)
    if row == (game_conf.len_each_side - 1):
        adjacent_set.remove(down)
    if column == 0:
        adjacent_set.remove(left)
    if column == (game_conf.len_each_side - 1):
        adjacent_set.remove(right)
    return adjacent_set


class Player(ndb.Model):
    """use a player model instead of a score model"""
    # playerID = ndb.IntegerProperty(required=True)
    score = ndb.FloatProperty(default=1000)
    playerName = ndb.StringProperty(required=True)
    wins = ndb.IntegerProperty(default=0)
    loses = ndb.IntegerProperty(default=0)


# class Board(ndb.Model):
#     """"""
# positions = msgprop.EnumProperty(go169Message.StoneMessage, repeated=True)


class Match(ndb.Model):
    """board_moves: """
    black_player = ndb.KeyProperty(Player, required=False)  # not required because a match should be joined first.
    white_player = ndb.KeyProperty(Player, required=False)  # not required because a match should be joined first.
    # matchID = ndb.IntegerProperty(required=True)
    is_outdated = ndb.BooleanProperty(default=False)
    # board_status = ndb.IntegerProperty(repeated=True,)
    # moves = msgprop.EnumProperty(go169Message.StoneMessage, repeated=True)
    moves = ndb.StringProperty(default="")
    nodes = msgprop.EnumProperty(go169Message.StoneMessage, repeated=True)

    def __init__(self):
        super.__init__()
        self.nodelist = self.nodes  # todo get a nodelist
        self.has_eliminated_at_least_one_enemy = False
        self.initiate_board()
        self.current_turn_color = ColorSideMessage.black
        # self.moves = []

    # start_playerID is not needed because match always starts with black side.
    # start_playerID = msgprop.EnumProperty(go169Message.ColorSideMessage ,required=True)
    def get_player_color(self, player_key):
        if player_key == self.black_player:
            return ColorSideMessage.black
        if player_key == self.white_player:
            return ColorSideMessage.white
        return None

    def get_adjacent_friends(self, position):
        this_node = self.get_node_from_position(position)
        wanted_node = this_node
        if this_node == StoneMessage.black_stone_just_put or this_node == StoneMessage.white_stone_just_put:
            wanted_node = this_node - 5
        adjacent_position_set = get_adjacent_position_set(position)
        adjacent_friend_set = set()
        for pos in adjacent_position_set:
            if self.get_node_from_position(pos) == wanted_node:
                adjacent_friend_set.add(pos)
        return adjacent_friend_set

    def get_adjacent_enemies(self, position):
        this_node = self.get_node_from_position(position)
        wanted_node = 3 - this_node
        if this_node == StoneMessage.black_stone_just_put or this_node == StoneMessage.white_stone_just_put:
            wanted_node = 8 - this_node
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
        return self.nodelist[position]

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
            self.nodelist[position] = StoneMessage.black_stone_just_put
        else:
            self.nodelist[position] = StoneMessage.white_stone_just_put

        if self.get_node_from_position(position) != StoneMessage.no_stone:
            # send_failure_invalid_move() #todo
            return
        enemies = self.get_adjacent_enemies(position)
        for enemy in enemies:
            if self.nodelist[enemy] == StoneMessage.no_stone:
                continue
            dead_enemy_chain = self.position_chain_dead(enemy)
            if dead_enemy_chain:
                # todo not sure there is something to do here
                for chain_component in dead_enemy_chain:
                    self.has_eliminated_at_least_one_enemy = True
                    self.nodelist[chain_component] = StoneMessage.no_stone
        if self.has_eliminated_at_least_one_enemy:
            # todo send sucess
            # todo send board nodes
            self.successful_move(position, color)
        else:
            self_dead_chain = self.position_chain_dead(position)
            if self_dead_chain:
                # todo send failure_invalid_move
                self.nodelist[position] = StoneMessage.no_stone
                return
            else:
                self.successful_move(position, color)

    def successful_move(self, position, color):
        self.moves += "%s,%s|" % (position, color)
        self.put()
        # todo start counting time (so send mail after 1 hour)

    def initiate_board(self):
        """initiate board. length of each side is defined in game_conf"""
        positions = game_conf.len_each_side * game_conf.len_each_side
        for i in range(1, positions):
            self.nodes[i] = StoneMessage.no_stone



@endpoints.api("Go169API", version=1, allowed_client_ids=[game_conf.CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID])
class Go169API(endpoints.remote.Service):

    create_game


    join_game

    roll_color

    surrender
    get_replay
    update_score
    get_leaderboard
    get_player_score




"""black starts first"""


@endpoints.method(request_message=messages.)


APPLICATION = endpoints.api_server([Go169API],
                                   restricted=False)
