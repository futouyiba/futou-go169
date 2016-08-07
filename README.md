This is a backend API project for ancient eastern board game "GO", which includes a backend without front end.

The game is played by 2 players, ideally 2 google users, take turns to put stones, black and white, to the board.
There is no time limit for each player each turn.

1. Front end ask for the board status. This API sends the specific
2.



## Products
- [App Engine][1]

## Language 
- [Python][2]

## APIs
- [Google Cloud Endpoints][3]

## Setup Instructions

1. Make sure to have the [App Engine SDK for Python][4] installed, version
   1.7.5 or higher.
2. Change `'YOUR-CLIENT-ID'` in [`static/js/render.js`][5] and
   [`tictactoe_api.py`][6] to the respective client ID(s) you have registered
   in the [APIs Console][7].
3. Update the value of `application` in [`app.yaml`][8] from `your-app-id`
   to the app ID you have registered in the App Engine admin console and would
   like to use to host your instance of this sample.
4. Run the application, and ensure it's running by visiting your local server's
   admin console (by default [localhost:8080/_ah/admin][9].)
5. Test your Endpoints by visiting the Google APIs Explorer:
  [localhost:8080/_ah/api/explorer][10]

[1]: https://developers.google.com/appengine
[2]: http://python.org/