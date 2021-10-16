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
  - watching status <small>(`unwatched`, `planned`, `watching`, `dropped`, `finished`)</small>
- **Eases**
  - opening website of series
  - playing the next episode
  - applying a naming convention to the episodes

### Arguements

- `--player`, `-p`
  - only affects 'play' mode
- `--fav`, `-f`
- `--rename`, `-r`
- `--status`, `-s`

### Commands

- `create <title>`
- `init`
  - ep count
  - website
  - original file format
- `open`
- `info`

### Contents of `.play.json`

- watched: `Int`
- epCount: `Int?`
- episodeDir: `FilePath`
- website: `String?`
- format: `RegEx` - The format of the downloaded episodes
- status: `enum Status`
- fav: `boolean`

### Contents of `.play-next.config`

- targetFormat: `StringTemplate`
- targetDir: `FilePath`
- dataSourceDir: `FilePath`
