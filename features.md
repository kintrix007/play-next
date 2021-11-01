# Play Next
### A command line utility for managing your series progress

---

### Command Line Arguments

The command line arguments are separated my whitespaces.

- A string of letters prefixed with two dashes (e.g `--version`)
- Single letter arguments prefixed with a single dash (e.g `-V`)
- Stacking single letter arguments (e.g `-fs`) \
  is interpreted the same as typing `-f -s`
- Marking the end of command line arguments explicitly with two dashes. (e.g `--`) \
  Might be added later

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

### Contents of `.play.json`

- title: `String`
- watched: `Int`
- ep_count: `Int?`
- website: `String?`
- format: `RegEx` - The format of the downloaded episodes
- status: `enum Status`
- starred: `Boolean`
- episode_dir: `AnyFilePath?`

### Contents of `.play-next.config`

- default_source_format: `RegEx`
  - default value: `^(?:[^\d]*\d+){0}[^\d]*0*(?P<ep>\d+).*\.(?P<ext>[\w\d]+)$`
- target_dir: `AbsoluteFilePath`
- source_dir: `AbsoluteFilePath`
- default_episode_dir: `AnyFilePath`

### Arguments

- `--with`, `-w`
  - only affects 'play' and 'open' mode
- `--full`, `-f`
  - only affects 'info'

### Commands

- `config` - can be used for reconfig, should update everything accordingly
- `create <title>`
  - ep count
  - website
  - original file format
  - episode dir
- `reinit`
  - same as `create`
- `open`
  - open series website
- `status <new status>`
  - sets the status to `new status`. Possible values are:
    - **planned** - *default*
    - **watching** - *automatically gets set after watching **first** ep*
    - **dropped**
    - **finished** - *automatically gets set after watching **last** ep*
- `link`
  - remake, update the symlinks
- `rename`
  - make the filenames of the episodes match the convention
- `star`
  - star a series
- `unstar`
  - star a series
- `info`
- `play` - *default*

### Example commands

- `play-next create komi-san-wa-comyushou-desu`
- `play-next create overlord`
- `play-next reinit`
- `play-next link`
- `play-next rename`
- `play-next`
- `play-next` or `play-next play` or `play-next --with vlc`
- `play-next open` or `play-next open --with firefox`
- `play-next info`
- `play-next info --full`
- `play-next status dropped`
- `play-next star`, `play-next unstar`
