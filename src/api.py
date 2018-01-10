from eve import Eve
app = Eve(settings='api_settings.py')

if __name__ == '__main__':
    app.run()
