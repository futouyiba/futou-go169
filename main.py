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
from game_conf import len_each_side, WEB_CLIENT_ID, ANDROID_AUDIENCE, \
    ANDROID_CLIENT_ID, IOS_CLIENT_ID
from math import floor
from protorpc import remote
from protorpc.message_types import VoidMessage
from go169Message import ScoreResponseMessage, LeaderboardMessage, \
    PutStoneMessage, BoardStatusResponse, MatchMoves, MyMatchResponse, \
    JoinMatchRequest, MatchListResponse
from model import Match, GameList, Player
from random import randint
import os


EMAIL_SCOPE = endpoints.EMAIL_SCOPE
API_EXPLORER_CLIENT_ID = endpoints.API_EXPLORER_CLIENT_ID


def position_int_to_row_column(integer_postion):
    """takes in a integer postion and returns (row position, column position)
    integratedPosition: a position according to index in the board list"""
    row = floor(integer_postion / len_each_side)
    column = integer_postion - row * len_each_side
    return row, column


def get_user_id(user, id_type="email"):
    if id_type == "email":
        return user.email()
    if id_type == "oauth":
        auth = os.getenv('HTTP_AUTHORIZATION')
        bearer, token = auth.split()
        token_type = 'id_token'
        if #todo


def position_row_column_to_int(row, column):
    """takes row and column, gives the integer position back"""
    integer_position = row * len_each_side + column
    return integer_position


def get_adjacent_position_set(integrate_position):
    """returns a set including all the adjacent positions,
     which could be up to 4 positions,
    and down to 2 positions since the board has borders"""
    up = integrate_position - len_each_side
    down = integrate_position + len_each_side
    left = integrate_position - 1
    right = integrate_position + 1
    adjacent_position_list = [up, down, left, right]
    adjacent_set = set(adjacent_position_list)
    row, column = position_int_to_row_column(integrate_position)
    if row == 0:
        adjacent_set.remove(up)
    if row == (len_each_side - 1):
        adjacent_set.remove(down)
    if column == 0:
        adjacent_set.remove(left)
    if column == (len_each_side - 1):
        adjacent_set.remove(right)
    return adjacent_set


@endpoints.api(
    name="go169", version='v1', audiences=[ANDROID_AUDIENCE],
    allowed_client_ids=[WEB_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID,
                        ANDROID_CLIENT_ID, IOS_CLIENT_ID],
    scopes=[EMAIL_SCOPE])
class Go169Api(remote.Service):

    def _copy_board_to_message(self, matchID):
        match = Match.get_by_id(matchID)
        nodes = Match.nodes
        board_statuses = []
        for index, node in enumerate(nodes):
            board_statuses[index] = int(node)
        message = BoardStatusResponse(matchID=matchID,
                                      board_statuses=board_statuses)
        return message


    def _initiate_match(self, creator, joiner):
        rand = randint(0,1)
        if rand==0:
            match = Match(black_player=creator, white_player=joiner)
        else:
            match = Match(black_player=joiner, white_player=creator)
        match.initiate_board()
        game_list_key = GameList.query(player_key == creator).get().key
        game_list_key.delete()


    def _settle_match(self, winner_key, loser_key):
        """update win/loses and score of each player"""
        #todo use skill package to calculate score
        winner_key.get().wins += 1
        loser_key.get().loses += 1



    @endpoints.method(request_message=VoidMessage,
                      response_message=VoidMessage, path='outgame/create',
                      http_method='POST', name="createGame")
    def create_game(self, request):
        user = endpoints.get_current_user()



    @endpoints.method
    def cancel_create_game

    @endpoints.method
    def join_game



    @endpoints.method
    def put_stone

    @endpoints.method
    def surrender
        self._settle_match

    @endpoints.method
    def get_leaderboard


    @endpoints.method
    def get_player_score


    @endpoints.method
    def get_replay

    # create_game
    #
    #
    # join_game
    #
    # roll_color
    #
    # surrender
    # get_replay
    # update_score
    # get_leaderboard
    # get_player_score




"""black starts first"""


# @endpoints.method(request_message=messages.)


# APPLICATION = endpoints.api_server([Go169API],
#                                    restricted=False)
