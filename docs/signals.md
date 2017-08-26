# Signals in Pinax Badges

## Module: `pinax.badges.signals`

`pinax-badges` makes one signal available to developers.

### `badge_awarded`

This signal is sent whenever a badge is awarded to a user.  It provides a
single argument, `badge`, which is an instance of `pinax.badges.models.BadgeAwarded`.
