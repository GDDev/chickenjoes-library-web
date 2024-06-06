<h1>Here is a little guide on how to run this app</h1>

<h4>
<span><bold>!IMPORTANT!</span></bold>
You must have Python and PIP installed for this project.
</h4>

To begin, clone this repository:
```
git clone git@github.com:GDDev/chickenjoes-library-web.git
```

After cloning, access the project's folder:
```
cd .\chickenjoes-library-web\
```

Now it's advised that you create a virtual environment:
```
python -m venv .venv
```

And activate it (if on Windows):
```
.\.venv\Scripts\activate
```

Then, you can install the requirements for this project:
```
python -m pip install -r requirements.txt
```

Once that's out of the way, you should be able to launch the localhost server:
```
python manage.py runserver
```

Hope this helps 🙃

<!-- <ol>
    <h2>
        <li> To Register a Book:</li>
    </h2>
    <ul>
        <li>Create an Author or find an existing one;</li>
        <span>Obs: Authors can't exist without a book.</span>
        <li>Inform the book data.</li>
    </ul>
    <h2>
        <li> To Register a Customer: </li>
    </h2>
    <ul>
        <li>Don't know yet.</li>
    </ul>
</ol> -->