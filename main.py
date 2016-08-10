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
from go169Message import
import game_conf
from protorpc import messages
from math import floor


class Player(ndb.Model):
    """use a player model instead of a score model"""
    playerID = ndb.IntegerProperty(required=True)
    score = ndb.FloatProperty(default=1000)
    playerName = ndb.StringProperty(required=True)
    wins = ndb.IntegerProperty(default=0)
    loses = ndb.IntegerProperty(default=0)


class Board(ndb.Model):
    """"""
    nodes = msgprop.EnumProperty(go169Message.StoneMessage, repeated=True)

class Match(ndb.Model):
    """board_moves: """
    black_player = ndb.KeyProperty(Player, required=False) # not required because a match should be joined first.
    white_player = ndb.KeyProperty(Player, required=False) # not required because a match should be joined first.
    matchID = ndb.IntegerProperty(required=True)
    is_outdated = ndb.BooleanProperty(default=False)
    board_status = ndb.IntegerProperty(repeated=True,)
    board_moves = msgprop.EnumProperty(go169Message.StoneMessage, repeated=True)
    # start_playerID is not needed because match always starts with black side.
    # start_playerID = msgprop.EnumProperty(go169Message.ColorSideMessage ,required=True)



    def make_move(self, postion, color):
        """change the board status & add a record in board moves."""


    @staticmethod
    def position_int_to_row_column(integer_postion):
        """takes in a integer postion and returns (row position, column position)
        integratedPosition: a position according to index in the board list"""
        row = floor(integer_postion/game_conf.len_each_side)
        column = integer_postion - row*game_conf.len_each_side
        return row, column

    @staticmethod
    def position_row_column_to_int(row, column):
        """"""
        integer_position = row*game_conf.len_each_side+column
        return integer_position

    @staticmethod
    def getAdjacentPositions(integratePosition):
        """returns a list including all the adjacent postions, it could be up to 4 positions,
        and down to 2 positions since the board has borders"""
        #todo
        up = integratePosition - game_conf.len_each_side
        down = integratePosition + game_conf.len_each_side
        left = integratePosition - 1
        right = integratePosition + 1
        row, column = Match.position_int_to_row_column(integratePosition)
        if row == 0:
            up = None
        if row == (game_conf.len_each_side-1):
            down = None
        if column == 0:
            left = None
        if column == (game_conf.len_each_side-1):
            right = None
        return up, down, left, right




class StoneChain(ndb.Model):
    #todo : should this be a ndb.Model?
    stones = ndb.KeyProperty



class Position(ndb.Model):
    """"""
    #todo : should this be a ndb.Model?
    position_integrated = ndb.IntegerProperty(required=True)

    position_status = msgprop.EnumProperty(go169Message.StoneMessage)

    @property
    def position_row(self):


@endpoints.api("Go169", version=1,allowed_client_ids=[game_conf.CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID])
class Go169API(endpoints.remote.Service):

    def initiate_board(self):
        """initiate board. length of each side is defined in game_conf"""
        # TODO-Should it be a static method?
        for row in range(1, game_conf.len_each_side):
            for column in range(1, game_conf.len_each_side):




"""black starts first"""

@endpoints.method(request_message=messages.)





APPLICATION = endpoints.api_server([TicTacToeApi],
                                   restricted=False)
