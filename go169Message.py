"""ProtoRPC messages for Go169 game."""

from protorpc import messages


class StoneMessage(messages.Enum):
    black_stone_before = 1
    white_stone_before = 2
    no_stone = 0
    black_stone_just_put = 6
    white_stone_just_put = 7
    black_stone_eliminated = 4
    white_stone_eliminated = 5


class ColorSideMessage(messages.Enum):
    black = 0
    white = 1


class ScoreResponseMessage(messages.Message):
    """ProtoRPC message definition to represent a see-user-score response."""
    user_id = messages.IntegerField(1, required=True)
    user_name = messages.StringField(2)
    score = messages.FloatField(3)


class LeaderboardMessage(messages.Message):
    """ProtoRPC message definition to represent a list of stored scores."""
    scores = messages.MessageField(ScoreResponseMessage, 1, repeated=True)


class PutStoneMessage(messages.Message):
    """ProtoRPC message definition to represent a put-stone request."""
    position = messages.IntegerField(1, required=True)
    matchID = messages.IntegerField(2, required=True)
    stoneType = messages.EnumField(StoneMessage, 3, required=True)


class BoardStatusResponse(messages.Message):
    """ProtoRPC message definition to represent a reponse giving
     all board status within it.
    Since the data isn't big for the whole board,
     to prevent cheating and un-sync issues,
    directly transfer all the board status."""
    position_statuses = messages.IntegerField(1, repeated=True)
    matchID = messages.IntegerField(2)


class MatchMoves(messages.Message):
    """Proto message giving a step by step information
     for frontend to replay match."""
    matchID = messages.IntegerField(2)
    moves = messages.MessageField(PutStoneMessage, 1, repeated=True)


class MyMatchResponse(messages.Message):
    """Proto message to give back the matchID"""
    matchID = messages.IntegerField(1)


class JoinMatchRequest(messages.Message):
    """proto message to request to join a match"""
    match_id = messages.IntegerField(1, required=False)


class MatchListResponse(messages.Message):
    """proto message to return a match list"""
    match_ids = messages.IntegerField(1, repeated=True)

class CancelCreateGameRequest(messages.Message):
    """proto message to cancel creating a game"""
    #todo need it?
    pass