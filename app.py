import streamlit as st
import json
import time

class Block:
    def __init__(self, index, timestamp, data, previous_block_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_block_hash = previous_block_hash
        self.hash = None

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True, cls=BlockEncoder)
        return str(hash(block_string))

class BlockEncoder(json.JSONEncoder):
    def default(self, o): 
        if isinstance(o, Block):
            return o.__dict__
        return super().default(o)

class BlockDecoder(json.JSONDecoder):
    def object_hook(self, d):
        if 'index' in d and 'timestamp' in d and 'data' in d and 'previous_block_hash' in d and 'hash' in d:
            block = Block(d['index'], d['timestamp'], d['data'], d['previous_block_hash'])
            block.hash = d['hash']
            return block
        return d

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), {"message": "Genesis Block"}, "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_block_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_block_hash != previous_block.hash:
                return False
        return True

class MovieTicket:
    def __init__(self, movie_name, ticket_id, customer_name):
        self.movie_name = movie_name
        self.ticket_id = ticket_id
        self.customer_name = customer_name

class MovieTicketBookingSystem:
    def __init__(self):
        self.blockchain = Blockchain()
        self.pending_transactions = []

    def book_ticket(self, movie_name, ticket_id, customer_name):
        ticket = MovieTicket(movie_name, ticket_id, customer_name)
        self.pending_transactions.append(ticket)
        self.mine_pending_transactions()

    def mine_pending_transactions(self):
        new_block = Block(
            len(self.blockchain.chain), 
            time.time(),   
            self.pending_transactions,
            self.blockchain.get_latest_block().hash)
        self.blockchain.add_block(new_block)
        self.pending_transactions = []

    def get_ticket_count(self):
        return len(self.blockchain.get_latest_block().data)

    def display_tickets(self):
        for block in self.blockchain.chain:
            if isinstance(block.data, list):
                for ticket in block.data:
                    st.write("Movie:", ticket.movie_name)
                    st.write("Ticket ID:", ticket.ticket_id)
                    st.write("Customer:", ticket.customer_name)
                    st.write("---")
            else:
                st.write("Message:", block.data["message"])
                st.write("---")

    def display_blockchain(self):
        for block in self.blockchain.chain:
            st.write("Block:", block.index)
            st.write("Timestamp:", block.timestamp)
            st.write("Data:", block.data)
            st.write("Previous Block Hash:", block.previous_block_hash)
            st.write("Hash:", block.hash)
            st.write("---")

booking_system = MovieTicketBookingSystem()

def main():
    st.title("Movie Ticket Booking System")

    menu = st.sidebar.selectbox("Menu", ["Book Ticket", "Display Tickets", "Display Blockchain"])

    if menu == "Book Ticket":
        st.header("Book Ticket")
        movie_name = st.text_input("Enter movie name:")
        ticket_id = st.text_input("Enter ticket ID:")
        customer_name = st.text_input("Enter customer name:")

        if st.button("Book Ticket"):
            booking_system.book_ticket(movie_name, ticket_id, customer_name)
            st.success("Ticket booked successfully!")

    elif menu == "Display Tickets":
        st.header("Booked Tickets")
        tickets = booking_system.blockchain.get_latest_block().data

        if tickets:
            for ticket in tickets:
                st.write("Movie:", ticket.movie_name)
                st.write("Ticket ID:", ticket.ticket_id)
                st.write("Customer:", ticket.customer_name)
                st.write("---")
        else:
            st.info("No tickets booked yet.")

    elif menu == "Display Blockchain":
        st.header("Blockchain")
        blocks = booking_system.blockchain.chain

        if blocks:
            for block in blocks:
                st.write("Block:", block.index)
                st.write("Timestamp:", block.timestamp)
                st.write("Data:", block.data)
                st.write("Previous Block Hash:", block.previous_block_hash)
                st.write("Hash:", block.hash)
                st.write("---")
        else:
            st.info("Blockchain is empty.")

if __name__ == "__main__":
    main()
