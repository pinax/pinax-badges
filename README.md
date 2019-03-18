![](http://pinaxproject.com/pinax-design/patches/pinax-badges.svg)

# Pinax Badges

[![](https://img.shields.io/pypi/v/pinax-badges.svg)](https://pypi.python.org/pypi/pinax-badges/)

[![CircleCi](https://img.shields.io/circleci/project/github/pinax/pinax-badges.svg)](https://circleci.com/gh/pinax/pinax-badges)
[![Codecov](https://img.shields.io/codecov/c/github/pinax/pinax-badges.svg)](https://codecov.io/gh/pinax/pinax-badges)
[![](https://img.shields.io/github/contributors/pinax/pinax-badges.svg)](https://github.com/pinax/pinax-badges/graphs/contributors)
[![](https://img.shields.io/github/issues-pr/pinax/pinax-badges.svg)](https://github.com/pinax/pinax-badges/pulls)
[![](https://img.shields.io/github/issues-pr-closed/pinax/pinax-badges.svg)](https://github.com/pinax/pinax-badges/pulls?q=is%3Apr+is%3Aclosed)

[![](http://slack.pinaxproject.com/badge.svg)](http://slack.pinaxproject.com/)
[![](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)


## Table of Contents

* [About Pinax](#about-pinax)
* [Overview](#overview)
  * [Supported Django and Python versions](#supported-django-and-python-versions)
* [Documentation](#documentation)
  * [Installation](#installation)
  * [Usage](#usage)
  * [Asynchronous Badges](#asynchronous-badges)
  * [Models](#models)
  * [Signals](#signals)
  * [Template Tags](#template-tags)
  * [Templates](#templates)
* [Change Log](#change-log)
* [History](#history)
* [Contribute](#contribute)
* [Code of Conduct](#code-of-conduct)
* [Connect with Pinax](#connect-with-pinax)
* [License](#license)


## About Pinax

Pinax is an open-source platform built on the Django Web Framework. It is an ecosystem of reusable
Django apps, themes, and starter project templates. This collection can be found at http://pinaxproject.com.


## pinax-badges

### Overview

As a reusable Django app, `pinax-badges` provides the ecosystem with
a well tested, documented, and proven badges application for awarding badges
to users in Django.

It provides simple abstractions over awarding users badges for completing tasks,
including multi-level badges, and repeatable badges, making it super simple to
add badges to a Django project.

#### Supported Django and Python versions

Django \ Python | 2.7 | 3.4 | 3.5 | 3.6
--------------- | --- | --- | --- | ---
1.11 |  *  |  *  |  *  |  *  
2.0  |     |  *  |  *  |  *


## Documentation

### Installation

Install the development version:

```shell
    $ pip install pinax-badges
```

Add `pinax.badges` to your `INSTALLED_APPS` setting:

```python
    INSTALLED_APPS = [
        # other apps
        "pinax.badges",
    ]
```

Add `pinax.badges.urls` to your project urlpatterns:

```python
    urlpatterns = [
        # other urls
        url(r"^badges/", include("pinax.badges.urls", namespace="pinax_badges")),
    ]
```

### Usage

#### `pinax.badges.base.Badge`

Pinax Badges works by allowing you to define your badges as subclasses of a
common `Badge` class and registering them with `pinax-badges`.  For example if
your site gave users points, and you wanted to award three ranks of badges
based on how many points a user had your badge might look like this:

```python
    from pinax.badges.base import Badge, BadgeAwarded
    from pinax.badges.registry import badges

    class PointsBadge(Badge):
        slug = "points"
        levels = [
            "Bronze",
            "Silver",
            "Gold",
        ]
        events = [
            "points_awarded",
        ]
        multiple = False

        def award(self, **state):
            user = state["user"]
            points = user.get_profile().points
            if points > 10000:
                return BadgeAwarded(level=3)
            elif points > 7500:
                return BadgeAwarded(level=2)
            elif points > 5000:
                return BadgeAwarded(level=1)


    badges.register(PointsBadge)
```

There are a few relevant attributes and methods here.

##### `slug`

The unique identifier for this `Badge`, it should never change.

##### `levels`

A list of the levels available for this badge (if this badge doesn't have
levels it should just be a list with one item).  It can either be a list of
strings, which are the names of the levels, or a list of
`pinax.badges.base.BadgeDetail` which have both names and description.

##### `events`

A list of events that can possibly trigger this badge to be awarded.  How
events are triggered is described in further detail below.

##### `multiple`

A boolean specifying whether or not this badge can be awarded to the same
user multiple times, currently if this badge has multiple levels this must
be `False`.

##### `award(self, **state)`

This method returns whether or not a user should be awarded this badge.
`state` is guarnteed to have a `"user"` key, as well as any other
custom data you provide.  It should return either a `BadgeAwarded`
instance, or `None`.  If this `Badge` doesn't have multiple levels
`BadgeAwarded` doesn't need to be provided an explicit level.

Note: _`BadgeAwarded.level` is 1-indexed._

Now that you have your `PointsBadge` class you need to be able to tell
Pinax Badges when to try to give it to a user.  To do this, any time a user
*might* have received a badge just call `badges.possibly_award_badge` with
the name of the event, and whatever state these events might need and
Pinax Badges will handle the details of seeing what badges need to be awarded
to the user:

```python
    from pinax.badges.registry import badges

    def my_view(request):
        if request.method == "POST":
            # do some things
            request.user.profile.award_points(15)
            badges.possibly_award_badge("points_awarded", user=request.user)
        # more view
```

By default badges will be awarded at the current time, if you need to overide
the award time of the badge you can pass a `force_timestamp` keyword argument
to `possibly_award_badge()`.

### Asynchronous Badges

**Important**
    To use asynchronous badges you must have [celery](http://github.com/ask/celery)
    installed and configured.

If your `Badge.award()` method takes a long time to compute it may be
prohibitively expensive to call during the request/response cycle.  To solve
this problem Pinax Badges provides an `async` option to `Badges`.  If this
is `True` Pinax Badges will defer calling your `award()` method, using
`celery`, and it will be called at a later time, by another process (read the
[celery docs](http://celeryproject.org/docs/) for more information on how
`celery` works).

Because `award()` won't be called until later you can define a `freeze()`
method which allows you to provide and additional state that you'll need to
compute `award()` correctly.  This may be necessary because your `Badge`
requires some mutable state.

```python
    class AddictBadge(Badge):
        # stuff
        async = True

        def freeze(self, **state):
            state["current_day"] = datetime.today()
            return state
```

In this example badge the user will be awarded the `AddictBadge` when they've
visited the site every day for a month, this is expensive to calculate so it
will be done outside the request/response cycle.  However, what happens if they
visit the site right before midnight, and then the `award()` method isn't
actually called until the next day?  Using the freeze method you can provide
additional state to the `award()` method.

### Models

#### Module: `pinax.badges.models`

##### `BadgeAward`

* `user` - The user who was awarded this badge.
* `awarded_at` - The `datetime` that this badge was awarded at.
* `slug` - The slug for the `Badge` that this refers to.
* `name` - The name for the `Badge` this refers to, for the appropriate level.
* `description` - The description for the `Badge` thsi refers to, for the appropriate level.

### Signals

#### Module: `pinax.badges.signals`

`pinax-badges` makes one signal available to developers.

##### `badge_awarded`

This signal is sent whenever a badge is awarded to a user.  It provides a
single argument, `badge`, which is an instance of `pinax.badges.models.BadgeAward`.

### Template Tags

#### Module: `pinax.badges.templatetags.pinax_badges_tags`

`pinax-badges` offers a number of templatetags for your convenience, which are
available in the `pinax_badges_tags` library.

##### `badge_count`

This tag returns the number of badges that have been awarded to this user, it
can either set a value in context, or simple display the count.  To display the
count its syntax is:

```django
    {% badge_count user %}
```

To get the count as a template variable:

```django
    {% badge_count user as badges %}
```

##### `badges_for_user`

This tag provides a `QuerySet` of all of a user's badges, ordered by when
they were awarded, descending, and makes them available as a template variable.
The `QuerySet` is composed of `pinax.badges.models.BadgeAward` instances.

```django
    {% badges_for_user user as badges %}
```

### Templates

Templates are supplied by the user, in a `pinax/badges/` subfolder in your project template search path.

#### `badges.html`

Lists all badges.

Context data:
A sorted iterable of badge dictionaries keyed by badge slug:

```python
"badges": 
[ 
    "<badge slug>": {
        "level": val,  # badge level
        "name": val,  # badge level name
        "description": val,  # badge level description
        "count": val,  # badge count
        "user_has": val,  # name and level of badges of this type earned by user
    },
]
``` 

#### `badge_detail.html`

Context data:

```python
"badge": badge,  # badge to be displayed
"badge_count": badge_count,  # number of times it has been awarded
"latest_awards": latest_awards,  # most recent awards of badge
```


## Change Log

### 2.0.0

* Add Django 2.0 compatibility testing
* Drop Django 1.8, 1.9, 1.10, and Python 3.3 support
* Add application URL namespacing
* Move documentation into README and standardize layout
* Convert CI and coverage to CircleCi and CodeCov
* Add PyPi-compatible long description


## History

It was built by [Eldarion](http://eldarion.com) as `brabeion` for use in [Typewar](http://typewar.com) and donated to Pinax in August 2017.


## Contribute

For an overview on how contributing to Pinax works read this [blog post](http://blog.pinaxproject.com/2016/02/26/recap-february-pinax-hangout/)
and watch the included video, or read our [How to Contribute](http://pinaxproject.com/pinax/how_to_contribute/) section.
For concrete contribution ideas, please see our
[Ways to Contribute/What We Need Help With](http://pinaxproject.com/pinax/ways_to_contribute/) section.

In case of any questions we recommend you join our [Pinax Slack team](http://slack.pinaxproject.com)
and ping us there instead of creating an issue on GitHub. Creating issues on GitHub is of course
also valid but we are usually able to help you faster if you ping us in Slack.

We also highly recommend reading our blog post on [Open Source and Self-Care](http://blog.pinaxproject.com/2016/01/19/open-source-and-self-care/).


## Code of Conduct

In order to foster a kind, inclusive, and harassment-free community, the Pinax Project
has a [code of conduct](http://pinaxproject.com/pinax/code_of_conduct/).
We ask you to treat everyone as a smart human programmer that shares an interest in Python, Django, and Pinax with you.


## Connect with Pinax

For updates and news regarding the Pinax Project, please follow us on Twitter [@pinaxproject](https://twitter.com/pinaxproject)
and check out our [Pinax Project blog](http://blog.pinaxproject.com).


## License

Copyright (c) 2012-2019 James Tauber and contributors under the [MIT license](https://opensource.org/licenses/MIT).
