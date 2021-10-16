# play-next
### A Command Line Utility for managing your progress watching a series

---

### Command Line Arguements

The command line arguements are separated my whitespaces.

- A string of letters prefixed with two dashes (e.g `--version`)
- Single letter arguements prefixed with a single dash (e.g `-V`)
- Stacking single letter arguements (e.g `-fs`) \
  is interpreted the same as typing `-f -s`
- Marking the end of command line arguements explicitly with two dashes. (e.g `--`)

### Features

- **Tracks**
  - episode count of series
  - episode progress in all series
  - favourites
  - watching status <small>(unwatched, planned, watching, dropped, finished)</small>
- **Eases**
  - opening website of series
  - playing the next episode
  - applying a naming convention to the episodes

### Arguements

- `--player`, `-p`
  - only affects 'play' mode
- `--fav`, `-f`
- `--rename`, `-r`

### Commands

- `create <title>`
- `init`
- `open`
- `info`
