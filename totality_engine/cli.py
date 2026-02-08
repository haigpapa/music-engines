import argparse
import sys
import json
import os
from sqlmodel import Session, create_engine, select, SQLModel
from totality_engine.engines.hit_science.pipeline import HitSciencePipeline
from totality_engine.engines.creative.audioscape import AudioscapeEngine
from totality_engine.engines.creative.lyrical import LyricalEngine
from totality_engine.engines.creative.composition import CompositionEngine
from totality_engine.engines.creative.album_architect import AlbumArchitectEngine
from totality_engine.engines.creative.context import ContextEngine

def handle_hit_science(args):
    pipeline = HitSciencePipeline()
    metadata = {
        "lyrics": args.lyrics,
        "artist_id": args.artist,
        "platform": args.platform,
        "target_markets": args.markets.split(",") if args.markets else []
    }
    
    try:
        results = pipeline.analyze_track(args.input, metadata)
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(f"Error: {e}")

def handle_creative(args):
    engine = None
    input_data = None
    
    if args.engine == "audioscape":
        engine = AudioscapeEngine()
        input_data = args.input
    elif args.engine == "lyrical":
        engine = LyricalEngine()
        input_data = args.input
    elif args.engine == "composition":
        engine = CompositionEngine()
        input_data = args.input
    elif args.engine == "album":
        engine = AlbumArchitectEngine()
        input_data = args.input
    elif args.engine == "context":
        engine = ContextEngine()
        input_data = {"file_path": args.input, "genre_key": args.genre}
    else:
        print(f"Unknown creative engine: {args.engine}")
        return

    print(f"--- Running {engine.__class__.__name__} ---")
    result = engine.analyze(input_data)
    print(json.dumps(result, indent=2))

def main():
    parser = argparse.ArgumentParser(description="Totality Engine CLI")
    subparsers = parser.add_subparsers(dest="command", help="Sub-command to run")

    # Hit Science Subcommand
    hs_parser = subparsers.add_parser("hit-science", help="Hit Science Analysis")
    hs_parser.add_argument("input", help="Audio file path")
    hs_parser.add_argument("--lyrics", help="Lyrics text", default="")
    hs_parser.add_argument("--artist", help="Artist ID", default="unknown_artist")
    hs_parser.add_argument("--platform", help="Target platform", default="Spotify")
    hs_parser.add_argument("--markets", help="Target markets (comma-separated)", default="US,UK")

    # Creative Subcommand
    creative_parser = subparsers.add_parser("creative", help="Creative Engines Analysis")
    creative_subparsers = creative_parser.add_subparsers(dest="engine", help="Creative Engine to use")
    
    # Audioscape
    p_audio = creative_subparsers.add_parser("audioscape", help="Technical Audio Analysis")
    p_audio.add_argument("input", help="Audio file path")

    # Lyrical
    p_lyric = creative_subparsers.add_parser("lyrical", help="Lyrical Analysis")
    p_lyric.add_argument("input", help="Lyrics file path")

    # Composition
    p_comp = creative_subparsers.add_parser("composition", help="Structural Analysis")
    p_comp.add_argument("input", help="Audio file path")

    # Album
    p_album = creative_subparsers.add_parser("album", help="Album Cohesion Analysis")
    p_album.add_argument("input", help="Directory path")

    # Context
    p_context = creative_subparsers.add_parser("context", help="Context/Genre Benchmarking")
    p_context.add_argument("input", help="Audio file path")
    p_context.add_argument("genre", help="Genre key for benchmarking")

    args = parser.parse_args()

    if args.command == "hit-science":
        handle_hit_science(args)
    elif args.command == "creative":
        handle_creative(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
