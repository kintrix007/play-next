module Lib
  ( cmdPlay
  ) where

import           Config
import           Data.Char   (isDigit)
import qualified Data.Text   as T
import           Series
import           System.Exit (ExitCode (ExitFailure), exitWith)
import           System.IO   (hPutStrLn, stderr)

cmdPlay :: Config -> Series -> [String] -> IO ()
cmdPlay config series args = do
  episodes <- getEpisodes config series
  let nextEp = progress series

  let matchingEps = filter ((== nextEp) . epNumber) episodes
  case matchingEps of
    [] -> undefined -- fail "No episodes found for " ++ show nextEp
    [ep] -> playFile ep
    _ -> do
      let description = "Multiple episodes match the next episode number (" ++ show nextEp ++ "):"
      idx <- promptForChoice description $ map (getEpString . epNumber) matchingEps
      playFile $ matchingEps !! idx

promptForChoice :: String -> [String] -> IO Int
promptForChoice text options = do
  putStrLn text
  putStrLn $ unlines $ zipWith (\n s -> show n ++ ": " ++ s) [1::Int ..] options
  inp <- T.unpack . T.strip . T.pack <$> getLine
  if all isDigit inp
    then return $ read inp - 1
    else do
      hPutStrLn stderr "Invalid option"
      exitWith $ ExitFailure 3


playFile :: Episode -> IO ()
playFile = undefined

getEpisodes :: Config -> Series -> IO [Episode]
getEpisodes _ _ = return []

data Episode = Episode
  { epNumber :: Progress
  , epTitle  :: String
  , epFile   :: FilePath
  } deriving (Show, Eq)

