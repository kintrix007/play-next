# Play Next
### A command line utility for managing your series progress

---

### Command Line Arguments

The command line arguments are separated by whitespaces.

- A string of letters prefixed with two dashes (e.g `--help`)
- Single letter arguments prefixed with a single dash (e.g `-h`)
- Stacking single letter arguments (e.g `-fs`) \
  is interpreted the same as typing `-f -s`
- Marking the end of command line arguments explicitly with two dashes. (e.g `--`)

### Features

- **Tracks for you**
  - episode count
  - episode progress in all series
  - favourites
  - watching status
- **Eases for you**
  - opening website of series
  - playing the next episode
  - applying a naming convention to the episodes

### Contents of `.play.json`

- title: `String`
- full_title: `String`
- watched: `Int`
- ep_count: `Int?`
- website: `String?`
- format: `RegEx` - The format of the downloaded episodes
- status: `enum Status`
- vid_source: `DirectoryPath?`

### Files that may or may not exist

- `starred` - if exists, the series is starred, otherwise not
- `seasonal` - if exists, the series is seasonal, otherwise not
- `local` - if exists, do not link to target dir, otherwise do

### Contents of `.play-next.config`

- default_source_format: `RegEx`
  - default value: `^(?:[^\d]*\d+){0}[^\d]*0*(?P<ep>\d+).*\.(?P<ext>[\w\d]+)$`
- target_dir: `AbsoluteFilePath`
- source_dir: `AbsoluteFilePath`
  - Ignore all subdirectories that start with a `.`
- default_vid_source: `DirectoryPath`
  - Looks at `default_episode_dir` and `.` for video files matching the name format
  - If not found, looks if `$PLAY_NEXT_EP_MASTER_DIR` has a subdirectory named the same as the title of the series
  - If found, looks for video files matching the name format
- website_template: `StringTemplate`
  - `{title}` will be replaced with the `full_title` of the series

---

### Commands

`--help`, `-h` is a valid flag for all commands

- `play` - *default command*
  - possible flags:
    - `--with <app>`, `-w <app>`
    - `--quiet`, `-q`
    
- `open`
  - possible flags:
    `--with <app>`, `-w <app>`
    - `--quiet`, `-q`
    
- `create <title>`
  - description
  - possible flags:
    - `--status <status>`, `-s <status>`
    - `--star`, `--fav`, `-f`
    - `--yes`, `-y`

- `reinit`
  - description
  - possible flags:
    - `--status <status>`, `-s <status>`
    - `--star`, `--fav`, `-f`
    - `--unstar`, `--unfav`, `-u`
    - `--yes`, `-y`

- `status <new status>`
  - possible flags:
    - `--verbose`, `-v`

- `list`
  - possible flags:
    - `--pretty`, `-p`

- `link`
  - possible flags:
    - `--verbose`, `-v`
    
- `rename`
  - possible flags:
    `--yes`, `-y`

- `star`
  - possible flags:
    `--verbose`, `-v`
    `--delete`, `-d`

---

### Example commands

- `play-next create komi-san-wa-comyushou-desu`
- `play-next create overlord --status watching --starred`
- `play-next reinit`
- `play-next link`
- `play-next rename`
- `play-next` or `play-next play` or `play-next --with vlc` or `play-next play --with vlc`
- `play-next open` or `play-next open --with xdg-open` or `play-next open --with firefox`
- `play-next info`
- `play-next info --verbose`
- `play-next status dropped`
- `play-next star`, `play-next unstar`
