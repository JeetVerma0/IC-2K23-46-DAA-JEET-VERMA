"""
Program 06: Music Playlist Manager Using a Circular Doubly Linked List
Course: IC-307D Data Structures and Algorithms Lab
Unit 3: Linked Lists (CO1)

This program models an interactive audio Playlist Manager using a
Circular Doubly Linked List (CDLL) from first principles:
- Each SongNode contains:
    1. title (str): Song title
    2. artist (str): Performing artist
    3. prev (SongNode): Pointer to preceding track in circular loop
    4. next (SongNode): Pointer to succeeding track in circular loop
- Architectural Design Decision:
    Why a Circular Doubly Linked List (CDLL)?
    In a standard Circular Singly Linked List, navigating to the preceding song
    (prev_song) requires an O(n) full traversal of the entire playlist until
    reaching the node where temp.next == current. In real-world media playback
    engines, "Skip to Previous Track" must execute instantaneously in O(1) time.
    Equipping each node with both 'prev' and 'next' references in a circular ring
    empowers O(1) forward and backward track skips, continuous loop replay, and
    O(1) active song deletions without auxiliary array allocation.
- Full edge case coverage:
    Handles empty playlists, single-song continuous loops, and deletion of the
    currently playing track.
- Interactive menu and automated test suite (--test flag).
"""

import sys
from typing import List, Optional, Tuple


class SongNode:
    """
    Represents an individual audio track in the circular playlist.

    Attributes:
        title: Title of the song.
        artist: Name of the artist or band.
        prev: Pointer to the preceding song in the loop.
        next: Pointer to the succeeding song in the loop.
    """

    def __init__(self, title: str, artist: str) -> None:
        self.title: str = title.strip()
        self.artist: str = artist.strip()
        self.prev: Optional["SongNode"] = None
        self.next: Optional["SongNode"] = None

    def __repr__(self) -> str:
        return f"SongNode('{self.title}' by '{self.artist}')"


class PlaylistManager:
    """
    Manages a circular music playlist supporting bidirectional playback,
    track insertion, removal, and search.

    Invariants:
        - For an empty playlist: current_song is None and _size == 0.
        - For a single-song playlist: node.next == node and node.prev == node.
        - For multiple songs: tail.next == head and head.prev == tail.
    """

    def __init__(self, name: str = "My Playlist") -> None:
        self.name: str = name
        self.current_song: Optional[SongNode] = None
        self._size: int = 0

    def is_empty(self) -> bool:
        """Checks whether the playlist contains any songs."""
        return self.current_song is None

    def song_count(self) -> int:
        """Returns the total number of songs in the playlist."""
        return self._size

    def __len__(self) -> int:
        return self._size

    def add_song(self, title: str, artist: str) -> None:
        """
        Appends a new song to the end of the circular playlist.
        If playlist was empty, the newly added song becomes current_song.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        clean_title = title.strip()
        clean_artist = artist.strip()
        if not clean_title or not clean_artist:
            raise ValueError("Song title and artist cannot be empty.")

        new_song = SongNode(clean_title, clean_artist)

        # 1. Empty playlist
        if self.current_song is None:
            new_song.next = new_song
            new_song.prev = new_song
            self.current_song = new_song
        # 2. Existing circular playlist
        else:
            # Let head = current_song, tail = current_song.prev
            head = self.current_song
            tail = head.prev
            assert tail is not None

            # Insert new_song between tail and head
            tail.next = new_song
            new_song.prev = tail
            new_song.next = head
            head.prev = new_song

        self._size += 1

    def remove_song(self, title: str) -> bool:
        """
        Removes the first song matching 'title' (case-insensitive) from the playlist.
        If the active song is deleted, current_song advances to the next track.

        Returns:
            True if song was found and removed; False otherwise.

        Time Complexity: O(n) search, O(1) pointer unlinking.
        Auxiliary Space Complexity: O(1)
        """
        if self.current_song is None:
            return False

        target_title = title.strip().lower()
        search_ptr = self.current_song
        found_node: Optional[SongNode] = None

        # Search around the circular ring
        while True:
            if search_ptr.title.lower() == target_title:
                found_node = search_ptr
                break
            search_ptr = search_ptr.next
            if search_ptr == self.current_song:
                break

        if found_node is None:
            return False

        # 1. Only one song in playlist
        if self._size == 1:
            self.current_song = None
        # 2. Multiple songs in playlist
        else:
            prev_node = found_node.prev
            next_node = found_node.next
            assert prev_node is not None and next_node is not None

            prev_node.next = next_node
            next_node.prev = prev_node

            # If deleting currently playing track, advance to next
            if self.current_song == found_node:
                self.current_song = next_node

        self._size -= 1
        return True

    def next_song(self) -> Optional[Tuple[str, str]]:
        """
        Advances to the next song in the circular playlist and returns (title, artist).
        Wraps around from end to beginning seamlessly.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        if self.current_song is None:
            return None

        self.current_song = self.current_song.next
        assert self.current_song is not None
        return self.current_song.title, self.current_song.artist

    def prev_song(self) -> Optional[Tuple[str, str]]:
        """
        Reverses to the preceding song in the circular playlist and returns (title, artist).
        Enabled in O(1) time by the Circular Doubly Linked List design.

        Time Complexity: O(1)
        Auxiliary Space Complexity: O(1)
        """
        if self.current_song is None:
            return None

        self.current_song = self.current_song.prev
        assert self.current_song is not None
        return self.current_song.title, self.current_song.artist

    def play_current(self) -> Optional[Tuple[str, str]]:
        """
        Simulates playback by returning the metadata of the current song.
        Does not play actual audio.
        """
        if self.current_song is None:
            return None
        return self.current_song.title, self.current_song.artist

    def search_song(self, title: str) -> Optional[Tuple[int, str, str]]:
        """
        Searches for a song by title (case-insensitive).

        Returns:
            (position_from_current, title, artist) if found, None otherwise.

        Time Complexity: O(n)
        Auxiliary Space Complexity: O(1)
        """
        if self.current_song is None:
            return None

        target = title.strip().lower()
        curr = self.current_song
        offset = 0

        while True:
            if curr.title.lower() == target:
                return offset, curr.title, curr.artist
            curr = curr.next
            offset += 1
            if curr == self.current_song:
                break

        return None

    def to_list(self) -> List[Tuple[str, str]]:
        """Traverses the circular playlist once starting from current_song."""
        result: List[Tuple[str, str]] = []
        if self.current_song is None:
            return result

        curr = self.current_song
        while True:
            result.append((curr.title, curr.artist))
            curr = curr.next
            if curr == self.current_song:
                break
        return result

    def display_playlist(self) -> None:
        """Prints a formatted track list with an indicator marking the playing track."""
        if self.current_song is None:
            print(f"\n[Playlist '{self.name}' is currently empty]")
            return

        print("\n" + "=" * 65)
        print(f"  PLAYLIST: {self.name} (Total Tracks: {self._size})")
        print("=" * 65)

        curr = self.current_song
        idx = 1
        while True:
            marker = " [PLAYING] ->" if curr == self.current_song else "             "
            print(f"{marker} Track {idx:2d}: '{curr.title}' by {curr.artist}")
            curr = curr.next
            idx += 1
            if curr == self.current_song:
                break

        print("=" * 65)


# ===========================================================================
# Automated Verification & Self-Tests
# ===========================================================================

def run_tests() -> None:
    """Executes comprehensive verification covering PlaylistManager operations and edge cases."""
    print("=" * 65)
    print("RUNNING COMPREHENSIVE TESTS: Playlist Manager (Program 06)")
    print("=" * 65)

    pm = PlaylistManager("Rock Anthems")

    # 1. Empty playlist operations
    assert pm.is_empty() is True
    assert pm.song_count() == 0
    assert pm.play_current() is None
    assert pm.next_song() is None
    assert pm.prev_song() is None
    assert pm.remove_song("Bohemian Rhapsody") is False
    assert pm.search_song("Hey Jude") is None
    print("  [Test 01 Passed] Initialized empty playlist verified.")

    # 2. Single-song playlist and self-referential cycle
    pm.add_song("Bohemian Rhapsody", "Queen")
    assert pm.song_count() == 1
    assert pm.play_current() == ("Bohemian Rhapsody", "Queen")

    # next_song and prev_song in single-song list should stay on same track
    assert pm.next_song() == ("Bohemian Rhapsody", "Queen")
    assert pm.prev_song() == ("Bohemian Rhapsody", "Queen")
    print("  [Test 02 Passed] Single-song continuous loop playback verified.")

    # 3. Multiple track additions
    pm.add_song("Stairway to Heaven", "Led Zeppelin")
    pm.add_song("Hotel California", "Eagles")
    pm.add_song("Sweet Child O' Mine", "Guns N' Roses")
    assert pm.song_count() == 4
    print("  [Test 03 Passed] Added multiple songs successfully.")

    # 4. Bidirectional circular navigation
    # Currently at track 1: Bohemian Rhapsody
    assert pm.play_current() == ("Bohemian Rhapsody", "Queen")

    # Forward skip
    assert pm.next_song() == ("Stairway to Heaven", "Led Zeppelin")
    assert pm.next_song() == ("Hotel California", "Eagles")
    assert pm.next_song() == ("Sweet Child O' Mine", "Guns N' Roses")

    # Wrap around forward: should loop back to track 1
    assert pm.next_song() == ("Bohemian Rhapsody", "Queen")

    # Backward skip (O(1) via CDLL prev pointer)
    # Wrap around backward from track 1 to last track
    assert pm.prev_song() == ("Sweet Child O' Mine", "Guns N' Roses")
    assert pm.prev_song() == ("Hotel California", "Eagles")
    print("  [Test 04 Passed] Forward and backward circular navigation verified.")

    # 5. Searching songs
    res = pm.search_song("hotel california")
    assert res is not None and res[1] == "Hotel California"

    missing = pm.search_song("Nonexistent Song")
    assert missing is None
    print("  [Test 05 Passed] Song search (present and absent) verified.")

    # 6. Song removal
    # Remove active track ("Hotel California") -> should advance to "Sweet Child O' Mine"
    assert pm.remove_song("Hotel California") is True
    assert pm.song_count() == 3
    assert pm.play_current() == ("Sweet Child O' Mine", "Guns N' Roses")

    # Remove non-active track
    assert pm.remove_song("Stairway to Heaven") is True
    assert pm.song_count() == 2

    # Remove until empty
    assert pm.remove_song("Sweet Child O' Mine") is True
    assert pm.remove_song("Bohemian Rhapsody") is True
    assert pm.is_empty() is True
    assert pm.current_song is None
    print("  [Test 06 Passed] Song removal and active track auto-advancement verified.")

    print("\nAll Program 06 automated tests PASSED successfully!")


def main() -> None:
    """Interactive command-line menu driver."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_tests()
        sys.exit(0)

    pm = PlaylistManager("Classic Rock Classics")

    # Pre-populate sample tracks
    pm.add_song("Bohemian Rhapsody", "Queen")
    pm.add_song("Hotel California", "Eagles")
    pm.add_song("Stairway to Heaven", "Led Zeppelin")
    pm.add_song("Comfortably Numb", "Pink Floyd")

    menu = """
========================================
     MUSIC PLAYLIST MANAGER (CO1)
========================================
1. Play Current Song (Display Metadata)
2. Next Track (Skip Forward)
3. Previous Track (Skip Backward)
4. Add New Song
5. Remove Song by Title
6. Search Song by Title
7. Display Full Playlist
8. Run Automated Self-Tests
9. Exit
========================================
"""

    while True:
        print(menu)
        choice = input("Enter choice (1-9): ").strip()

        if choice == "1":
            track = pm.play_current()
            if track:
                print(f"\n[NOW PLAYING] '{track[0]}' by {track[1]}")
            else:
                print("\nPlaylist is currently empty.")

        elif choice == "2":
            track = pm.next_song()
            if track:
                print(f"\n[NEXT TRACK] -> '{track[0]}' by {track[1]}")
            else:
                print("\nPlaylist is empty.")

        elif choice == "3":
            track = pm.prev_song()
            if track:
                print(f"\n[PREVIOUS TRACK] <- '{track[0]}' by {track[1]}")
            else:
                print("\nPlaylist is empty.")

        elif choice == "4":
            t = input("Enter song title: ").strip()
            a = input("Enter artist name: ").strip()
            try:
                pm.add_song(t, a)
                print(f"Added '{t}' by {a} to playlist.")
            except ValueError as err:
                print(f"Error: {err}")

        elif choice == "5":
            t = input("Enter title of song to remove: ").strip()
            if pm.remove_song(t):
                print(f"Removed '{t}' from playlist.")
            else:
                print(f"Song '{t}' was not found in playlist.")

        elif choice == "6":
            t = input("Enter title to search: ").strip()
            res = pm.search_song(t)
            if res:
                offset, title, artist = res
                print(f"Found: '{title}' by {artist} ({offset} tracks ahead of current)")
            else:
                print(f"'{t}' not found in playlist.")

        elif choice == "7":
            pm.display_playlist()

        elif choice == "8":
            run_tests()

        elif choice == "9":
            print("Exiting Playlist Manager. Enjoy your music!")
            break

        else:
            print("Invalid choice. Please select 1-9.")


if __name__ == "__main__":
    main()

