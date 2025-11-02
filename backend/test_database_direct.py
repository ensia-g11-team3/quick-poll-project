#!/usr/bin/env python3
"""
Simple script to view database contents
Run: python view_database.py
"""
import sqlite3
import os
import sys

def get_db_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'quick_poll_db.sqlite')


def show_all_polls(conn):
    """Show all polls"""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT poll_id, question, poll_link, created_at 
        FROM polls 
        ORDER BY created_at DESC
    ''')
    polls = cursor.fetchall()
    
    print("\n" + "="*80)
    print("ALL POLLS IN DATABASE")
    print("="*80)
    
    if polls:
        print(f"\n{'ID':<5} {'Question':<50} {'Link':<20} {'Created'}")
        print("-"*80)
        for poll in polls:
            question = poll[1][:47] + "..." if len(poll[1]) > 50 else poll[1]
            print(f"{poll[0]:<5} {question:<50} {poll[2]:<20} {poll[3]}")
        print(f"\nTotal: {len(polls)} polls")
    else:
        print("\nNo polls found")
    
    print()

def show_poll_details(conn, poll_link=None, poll_id=None):
    """Show detailed information about a specific poll"""
    cursor = conn.cursor()
    
    if poll_link:
        cursor.execute('SELECT poll_id, question, poll_link, created_at FROM polls WHERE poll_link = ?', (poll_link,))
    elif poll_id:
        cursor.execute('SELECT poll_id, question, poll_link, created_at FROM polls WHERE poll_id = ?', (poll_id,))
    else:
        print("Error: Need poll_link or poll_id")
        return
    
    poll = cursor.fetchone()
    
    if not poll:
        print(f"Poll not found")
        return
    
    poll_id = poll[0]
    
    print("\n" + "="*80)
    print(f"POLL DETAILS - ID: {poll_id}")
    print("="*80)
    print(f"Question: {poll[1]}")
    print(f"Link: {poll[2]}")
    print(f"Created: {poll[3]}")
    print()
    
    # Get options
    cursor.execute('SELECT option_id, option_text FROM options WHERE poll_id = ? ORDER BY option_id', (poll_id,))
    options = cursor.fetchall()
    
    print("Options:")
    for opt in options:
        # Get vote count
        cursor.execute('SELECT COUNT(*) FROM votes WHERE option_id = ?', (opt[0],))
        vote_count = cursor.fetchone()[0]
        print(f"  {opt[0]}. {opt[1]} - {vote_count} vote(s)")
    
    # Get total votes
    cursor.execute('SELECT COUNT(*) FROM votes WHERE poll_id = ?', (poll_id,))
    total_votes = cursor.fetchone()[0]
    print(f"\nTotal Votes: {total_votes}")
    print()

def show_poll_results(conn, poll_link=None, poll_id=None):
    """Show poll results with percentages"""
    cursor = conn.cursor()
    
    if poll_link:
        cursor.execute('SELECT poll_id FROM polls WHERE poll_link = ?', (poll_link,))
        result = cursor.fetchone()
        if not result:
            print(f"Poll with link '{poll_link}' not found")
            return
        poll_id = result[0]
    elif not poll_id:
        print("Error: Need poll_link or poll_id")
        return
    
    # Get poll question
    cursor.execute('SELECT question FROM polls WHERE poll_id = ?', (poll_id,))
    question = cursor.fetchone()[0]
    
    # Get results
    cursor.execute('''
        SELECT o.option_text, COUNT(v.vote_id) as vote_count
        FROM options o
        LEFT JOIN votes v ON o.option_id = v.option_id
        WHERE o.poll_id = ?
        GROUP BY o.option_id, o.option_text
        ORDER BY o.option_id
    ''', (poll_id,))
    results = cursor.fetchall()
    
    total_votes = sum(r[1] for r in results)
    
    print("\n" + "="*80)
    print(f"POLL RESULTS")
    print("="*80)
    print(f"Question: {question}")
    print()
    
    if results:
        for option_text, vote_count in results:
            percentage = round((vote_count / total_votes * 100) if total_votes > 0 else 0, 1)
            bar_length = int(percentage / 2)  # Scale to 50 chars
            bar = "=" * bar_length
            print(f"{option_text:<30} {vote_count:>3} votes ({percentage:>5.1f}%) [{bar}]")
    
    print(f"\nTotal Votes: {total_votes}")
    print()

def main():
    db_path = get_db_path()
    
    if not os.path.exists(db_path):
        print(f"Database not found at: {db_path}")
        print("Make sure the backend has been run at least once to create the database.")
        return 1
    
    try:
        conn = sqlite3.connect(db_path)
        
        # Check if specific poll requested
        if len(sys.argv) > 1:
            poll_link = sys.argv[1]
            if poll_link.startswith("http"):
                # Extract poll link from URL
                if "/poll/" in poll_link:
                    poll_link = poll_link.split("/poll/")[-1].split("/")[0]
            show_poll_results(conn, poll_link=poll_link)
        else:
            # Show all polls
            show_all_polls(conn)
            
            # Ask if user wants details
            print("\nTo view details of a specific poll, run:")
            print("  python view_database.py <poll_link>")
            print("\nExample:")
            print("  python view_database.py _4X04pztOuLOFw")
        
        conn.close()
        return 0
        
    except sqlite3.Error as e:
        print(f"Database error: {str(e)}")
        return 1
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
if __name__ == "__main__":
    sys.exit(main())