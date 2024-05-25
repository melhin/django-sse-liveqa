# Django  Server-Sent Events (SSE) LiveQA

A simple project to demonstrate building a Live QA app entirely on SSE.
This is only for demonstration and not necessarily a good production candidate


## How do you run this locally

* Setup Redis(If you want to run server separately)
```
make local-setup
```

* Otherwise run the whole application
```
make local
```

And then you are all set to go :)


### Running with Docker Compose
```
make start
```

### Getting Feed

```
 ./manage.py get_mastodon_feed --domain <DOMAIN>
```
Don't forget to add MASTODON_BEARER_TOKEN in your .env. Also maybe SECRET_KEY (for django)
