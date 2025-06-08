# pepper

## Pepper is a LLM based motivational tool
Pepper is designed to help someone with ADHD make the best use of their time by keeping them focused on what they can accomplish in the near term. It's not really intended for the public but I decided to share it anyway.


## Development
The steps here are temporary so I can get back to normal work in the meantime

1) Clone the repo
2) Create a .env file in the app directory
3) Add the following:
    OPENAI_API_KEY={your api key}
    DB_HOST={your odbc host}
    DB_NAME={your db name}
    DB_USER={your db user}
    DB_PASSWORD={your db password}
4) If you are intending to serve this somewhere other than your local machine, edit index.js to point the API_BASE_URL at wherever the api will be hosted
5) Run the SQL files in the sql directory against whatever database you plan on using. It should work no matter the flavor of DB but if you run into problems, chatGPT is your friend.
