# Template Tags in Pinax Badges

## Module: `pinax.badges.templatetags.pinax_badges_tags`

`pinax-badges` offers a number of templatetags for your convenience, which are
available in the `pinax_badges_tags` library.

### `badge_count`

This tag returns the number of badges that have been awarded to this user, it
can either set a value in context, or simple display the count.  To display the
count its syntax is:

```html
    {% badge_count user %}
```

To get the count as a template variable:

```html
    {% badge_count user as badges %}
```

### `badges_for_user`

This tag provides a `QuerySet` of all of a user's badges, ordered by when
they were awarded, descending, and makes them available as a template variable.
The `QuerySet` is composed of `pinax.badges.models.BadgeAwarded` instances.

```html
    {% badges_for_user user as badges %}
```
