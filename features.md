# Play Next
### A command line utility for manging your series progress

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
  - episode count
  - episode progress in all series
  - favourites
  - watching status
- **Eases**
  - opening website of series
  - playing the next episode
  - applying a naming convention to the episodes

### Arguements

- `--with`, `-w`
  - only affects 'play' and 'open' mode
- `--fave`, `-f`
  - favourite given series

### Commands

- `create <title>`
- `init`
  - ep count
  - website
  - original file format
- `open`
  - open series website
- `status <new status>`
  - sets the status to `new status`. Possible values are:
    - planned - *default*
    - watching - *automatically gets set after watching **first** ep*
    - dropped
    - finished - *automatically gets set after watching **last** ep*
- `sync`
  - sync the symlinks
- `rename`
  - make the filenames of the episodes match the convention

### Contents of `.play.json`

- title: `String`
- watched: `Int`
- ep_count: `Int?`
- website: `String?`
- format: `RegEx` - The format of the downloaded episodes
- status: `enum Status`
- fav: `Boolean`
- episode_dir: `FilePath?`

### Contents of `.play-next.config`

- target_format: `StringTemplate`
  - `{title}` for the user-specified title
  - `{0}`, `{1}`, `{2}`... for the user-specified RegEx matches in order
- default_source_format: `RegEx`
  - default value: \
    `^(?:[^\d]*\d+){0}[^\d]*0*(?P<episode>\d+).*\.(?P<extension>[\w\d]+)$`
- target_dir: `FilePath`
- source_dir: `FilePath`

### Example commands

- `play-next create komi-san-wa-comyushou-desu`
- `play-next create overlord --fave`
- `play-next init --fave`
  - initializes it, then adds it to the favorites.
- `play-next sync`
- `play-next rename`
- `play-next --fave`
  - adds current series to favourites, does **not** play.
- `play-next` or `play-next --with vlc`
- `play-next open` or `play-next open --with firefox`
- `play-next status`
- `play-next status dropped`
