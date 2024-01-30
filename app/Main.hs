module Main (main) where

import Lib
import System.Environment (getArgs)
import System.Exit (exitWith, ExitCode (ExitFailure))
import GHC.IO.Handle.Text (hPutStrLn)
import System.IO (stderr)

main :: IO ()
main = do
  (cmd, args) <- parseArgs <$> getArgs

  case cmd of
    "help" -> undefined
    "--help" -> undefined
    "play" -> undefined
    _ -> do
      hPutStrLn stderr $ "Invalid command: " ++ show cmd
      exitWith (ExitFailure 1)

parseArgs :: [String] -> (String, [String])
parseArgs _ = ("play", [])

