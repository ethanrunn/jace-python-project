from market import create_app
from market.database import migrate

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
