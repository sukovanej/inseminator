# Introduction

**Attention! The text might contain biased thoughts and could cause anxiety and
nose bleeding. It is full of hate and creepy ideas.**

The goal of this library is of course provide a simple tool for dependency injection.
But also it should motivate application developers to follow techniques resulting in
a well cohesive and minimally coupled code. If you are new to designing an application
by thinking about code coupling and cohesion I strongly recommend reading great
books from **R. C. Martin** (aka Uncle Bob) or **Martin Fowler**. 

I bet most developers are aware of the famous *Clean Code* and *Clean Architecture* books. 
While I don't want to be pedantic about all the details in these books I also hate the
state of mind like 

> Yeeeah, riiight. I mean it makes sense but this is not a Java or C# world, this is Python
> and the real pythonista doesn't think like that. Why don't you just use a dictionary and 
> instead of the class simply call requests and then do the flask mambo jambo and here we are
> in half the size of the Java code?

Doesn't it sound reasonable? Indeed, it does! The problem is we should sometime distiguish 
between implementation-based thinking and the desing / architectural one. Python is a great 
tool for expressing implementation in a very simple and human-readable way! It is awesome
language for very fast prototyping. The problem is that when you start the business application
from the very beginning you are not forced to think about the design of the application and
the main driver is very fast implementation and delivering to a customer. That is totally rasonable.

But sometimes you might feel like adding new features and introducing new colleages to the codebase
is very hard (as a consequence - expensive). When searching for a single thing in the code
you find yourself being in a package containing database queries and json output construction
for the API at the same time. Moreover the session object for a database is somehow magically
configured by another package and depending on import statements order and if you are lucky
you are able to get a pre-configured global session object in the import-time. And don't get me
wrong here - importing a preconfigured object is super easy and it can substantially speed up
your development if you *just import it*.

Importing global / singleton objects is fine except IT IS NOT!

## Example

I already summarized all the pros of using global objects - basically less typing, right...?
Let's see some code.

```Python
""" =================== log.py =================== """
import my_awesome_logger_library


logger = my_awesome_logger_library.get_logger()
logger.configure(incredibly_great_log_setup())


""" =================== db.py =================== """
# psycopg, sqla, or whatever db thing imports are there
engine = mambo_jambo()
session = scoped_session_magic(wtf=engine)


""" =================== api.py =================== """
from .db import session
from .log import logger


app = flask_or_whatever()


@app.route("my-awesome-route")
def endpoint_handler(body_input):
    logger.info("starting_the_business")
    objects = session.query(whatever)

    # another interesting logic
    # also lets call monitoring shit there
    # and probably some other APIs
    # and we should better also update something in the db

    return average_penis_length + 3
```

The code above is a simple API with an abillity to talk to database, save application
metrics, output logs and talk to another services (use your imagination). Actually it
doesn't look so bad and if I was writing a simple 100-line application with similar 
abbilities such a design would be sufficient and if it turned out we need to extend it,
it is not a big deal to rewrite 100-line Python application within a more robust design
decisions.

Now, let's imagine this piece of code is part of 10k-line long Python application. 

  - **ability to test** - somewhere from *zero* to *what the heck is automatic testing?*.
    Since everything is happening in the import-time you can use monkeypatching and hope
    the code will never change, that makes sense in the beginning but than you decide to
    change a single component of your system and you find out you have to delete all the
    tests because they are so tighly coupled to the inner implementation of your application
    so it is not usable even for a minor change. Also did I mention your tests will be
    broken and you will be repairing them all the time?

  - **ability to maintain** - you will spend half of your day searching when and where did
    the session object get configured and why is the connection pool limit set to 5 instead
    of 10. Bus factor seems to be around 0.

  - **ability to extend** - if you are okay with copy / paste and you are good in testing
    in a production then probably no problem.


Let's see something similar.

```Python
""" =================== log.py =================== """
import my_awesome_logger_library


def logger_factory():
    logger = my_awesome_logger_library.get_logger()
    logger.configure(incredibly_great_log_setup())
    return logger


""" =================== db.py =================== """
# psycopg, sqla, or whatever db thing imports are there
class Database:
    def __init__(self, connection_string, connection_pool_config)
        self.__engine = another_mambo_jambo(connection_string)
        self.session = scoped_session_magic(wtf=engine)


""" =================== domain.py =================== """
class Domain:
    def __init__(self, db, log):
        self.__db = db
        self.__log = log

    def do_business_logic(self, whatever_input_value):
        # awesome business logic
        # the loggin and monitoring can still be there
        # but preferebly passed through constructor
        return average_penis_length + 3


""" =================== api.py =================== """
from .domain import Domain


app = flask_or_whatever()


@app.route("my-awesome-route")
def endpoint_handler(body_input):
    domain = a_function_that_returns(Domain)
    return domain.do_business_logic(body_input["i-dont-care"])
```

Hopefully the simplification won't hide important concepts I aimed to ilustrate. Let's
summarize cons if this approach.

  - Now whoever is using `Database` class they must make sure it is prepared at the moment
    and somehow passed from the top. If no DI tool is used it might result in a complicated
    chain of passing a single instance from the top and we're not even talking about changing
    the signature of the class...

  - Basically we only moved the construction of our objects from their files to a single file
    and moreover now the initial preparation of the application can be duplicated if we reuse the
    same code for more types of application - usually API (flask) and async queueu (celery), we are
    forced to prepare all the dependencies for both of them.

  - obviously in the production it does the same thing like the previous implementation but
    using a slightly complicated code and more lines of it.

  - when dealing with the code we not only have to think about the code behaviour but also its
    dependencies because it is explicitly asking us to provide them through class constructors
    which is super annoying!

The good news is a lot of annoying problems mentioned above are solved by using factories or
injectors. Also it seems like these disadvantages rather disappear in a shine of the benefits.

  - The first awesome thing is we are doing absolutely nothing in the import time. The only
    potentially untestable places will be entrypoints. But it is not a big deal - the great news
    is we can easily test our domain logic because it is no longer coupled with the database and
    logs. We can easily mock them and test to domain layer objects independently of the infrastructure
    code. **By applying inversion of control we get testing for free!**

  - If we have tests it should be easier to maintain the application, also now the Domain class
    has a clear signature thus it is obvious what are the dependencies. Moreover, setup of some
    critical components like logging and database now probably happens in a single place - in the
    entrypoint or handler functions, it doesn't matter the key point is we have complete control
    over our code execution.
