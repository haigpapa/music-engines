import argparse
from sqlmodel import Session, create_engine, select, SQLModel
from totality_engine.core.schema import SongVersion
from totality_engine.engines.hit_science.core import HitScienceEngine

def main():
    parser = argparse.ArgumentParser(description="Hit Science Engine CLI")
    parser.add_argument("--version-id", type=int, help="ID of the song version to analyze")
    args = parser.parse_args()

    sqlite_url = "sqlite:///totality.db"
    engine = create_engine(sqlite_url)

    # Ensure tables exist
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # Check for seed data (simplified seeding logic for CLI)
        from totality_engine.core.schema import Song, SongVersion, AudioFeatures, LyricFeatures
        existing_song = session.exec(select(Song).where(Song.canonical_title == "Hit Science Demo")).first()
        if not existing_song:
            print("Seeding DB with Hit Science Demo Song...")
            song = Song(canonical_title="Hit Science Demo")
            version = SongVersion(song=song, version_type="original", duration_ms=210000)
            
            audio = AudioFeatures(
                version=version,
                tempo_bpm=130.0,
                time_signature=4,
                key_estimated=5,
                mode_estimated=0,
                loudness_lufs=-4.5,
                dynamic_range_db=4.0,
                spectral_centroid_avg=2200.0
            )
            lyrics = LyricFeatures(
                version=version,
                language_id="en",
                word_count=450,
                sentiment_valence=0.7,
                explicit_content=True
            )
            session.add(song)
            session.add(version)
            session.add(audio)
            session.add(lyrics)
            session.commit()
            print("Seeding complete.")

        hit_engine = HitScienceEngine(session)
        try:
            # If no version ID provided, find the first available
            if not args.version_id:
                version = session.exec(select(SongVersion)).first()
                if not version:
                    print("No song versions found in database.")
                    return
                print(f"No version ID provided. Analyzing first available version: {version.id}")
                version_id = version.id
            else:
                version_id = args.version_id

            report = hit_engine.analyze_version(version_id)
            print(report.model_dump_json(indent=2))
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
