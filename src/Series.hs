module Series
  ( Series (..)
  , Progress (..)
  , Status (..)
  , getEpString
  ) where

data Series = Series
  { seriesTitle :: String
  , seriesHumanTitle :: String
  , progress :: Progress
  , status :: Status
  , starred :: Bool
  , customEpDir :: Maybe FilePath
  , startSeason :: Maybe Season
  } deriving (Show, Eq)

data Season = Season Int Quarter
  deriving (Show, Eq)

data Quarter = Winter | Spring | Summer | Fall
  deriving (Show, Enum, Eq, Ord, Bounded)

data Progress
  = Numeric Int (Maybe Int)
  | Textual Int [String]
  deriving (Show, Eq)

getEpString :: Progress -> String
getEpString (Numeric n _) = show n
getEpString (Textual n names) = names !! (n - 1)

data Status = Planned | Watching | Finished | Dropped
  deriving (Show, Enum, Eq, Ord, Bounded)
