module Config
  ( Config (..)
  ) where

data Config = Config
  { configSourcePaths :: [FilePath]
  , configPlayer      :: Player
  } deriving (Show)

data Player = PlayerPath FilePath
            | PlayerCommand String
            deriving (Show)
