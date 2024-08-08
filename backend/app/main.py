"""
    ! READ BEFORE TO UNDERSTAND ANNOTATIONS 
    Download extenstion better comments https://marketplace.visualstudio.com/items?itemName=aaron-bond.better-comments to make it more visible on visual studio code
    Annotations are written as below:
        # Is used to understand single line comment example Import
        ! Is used to grab your attention to an important line
        ? Provides a list of functions 
        * * Is used to elobrate over a function 
"""

#  Used to make fast api development
import uvicorn
# Used to make api keys
from fastapi import FastAPI
# Middleware allows cross origin resource sharing for request
from fastapi.middleware.cors import CORSMiddleware
# import config file to get batabase 
from app.config import db
# Create inital role 
from app.service.auth_service import generate_role


# Defines the origins for api
origins= [
    "http://localhost:3000"
]

"""
    * This function initializes the application.
    It calls db.init() which establishes the database connection 
    It creates a FastAPI application instance with a title, description, and version.
    ! It configures CORS middleware to allow requests from the specified origins with all methods and headers.
    Under the @app.on_event("startup") decorator, it defines an asynchronous starup function that runs on application startup.
    * * Some tasks, like connecting to a database or loading initial data, can start running in the background while the application is getting ready to receive requests. 
    * * This can improve performance and responsiveness.
    * * The @app.on_event("startup") decorator marks a function to be run when the application starts. Inside this function, you can have tasks like:
        ? Connecting to the database.
                Inside starup, it calls db.create_all() which probably creates any necessary database tables based on models.
        ? Creating tables in the database.
                It also calls generate_role(), which might be used to create a default user role in the system.
        ? Loading initial data.
    Similarly, a shutdown function runs on application shutdown, closing the database connection.
    Finally, it imports routers from the authentication and users modules (containing login and user management logic) and includes them in the main application.
    The function returns the initialized FastAPI app.
"""

def init_app():
    db.init()

    app = FastAPI(
        title= "Trying login",
        description= "Login Page",
        version= "1"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    @app.on_event("startup")
    async def starup():
        await db.create_all()
        await generate_role()
    
    @app.on_event("shutdown")
    async def shutdown():
        await db.close()

    from app.controller import authentication, users

    app.include_router(authentication.router)
    app.include_router(users.router)

    return app

app = init_app()

"""
    ! app stores the initialized application instance returned by init_app.
    The start function defines the entry point for running the application.
    * * It uses uvicorn.run to launch the application using the following arguments:
    * * app.main:app: This points to the ASGI application (entry point for serving) defined in the app variable.
    * * host="localhost": Specifies the host to listen on (localhost in this case).
    * * port=8888: Defines the port to listen on (port 8888).
    * * reload=True: Enables automatic reloading of the application on code changes.
"""

def start():
    """Launched with 'poetry run start' at root level """
    uvicorn.run("app.main:app", host="localhost", port=8888, reload=True)