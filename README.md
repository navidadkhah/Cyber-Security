# Cyber Security Assignments
In this repository, we have three assignments about cyber security and cryptography in the network. Assignments are as follows:  
 - [Timing Convert Channel](#timing-convert-channel)
 - [Feistel Algorithm](#feistel-algorithm)

# Timing Convert Channel

This project implements a simple timing covert channel using Java's concurrency features. The channel allows for the transmission of binary messages based on different timing intervals, effectively simulating a covert communication mechanism.
<p align="center">
 <img src="https://github.com/user-attachments/assets/e980ffb2-6626-4c32-a07f-ac2b2f59f74e" width="600">
</p>

### Key Concepts

- **Covert Channel**: A communication channel that allows information to be communicated in a way that is not intended to be noticed by unauthorized entities.
- **Timing Channel**: This specific type of covert channel uses the timing of message transmission to convey information (e.g., longer transmission times for one bit and shorter for another).

## Code Explanation

### Classes and Structure

1. **TimingConvertChannel**: This class implements a blocking channel using a `BlockingQueue` to ensure thread-safe communication between the sender and receiver.

   - **Constructor**: Initializes the channel with a fixed size of 1.
   - **send(int timingInfo)**: Sends timing information through the channel. If the channel is full, it blocks until space becomes available.
   - **receive()**: Receives timing information from the channel. If the channel is empty, it blocks until an item is available.

2. **Sender**: Implements the `Runnable` interface to create a sender thread.

   - **run()**: Sends a predefined binary message ("1010") bit by bit. It uses different timing intervals to indicate the value of each bit:
     - **Bit 1**: Sent with a timing of 2 seconds.
     - **Bit 0**: Sent with a timing of 1 second.
   - Each bit's transmission is simulated by sleeping the thread for the corresponding amount of time.

3. **Receiver**: Also implements the `Runnable` interface to create a receiver thread.

   - **run()**: Receives timing information for a fixed number of bits (4 in this case) and reconstructs the binary message. The timing information is converted back into bits:
     - **Timing of 2 seconds** corresponds to Bit 1.
     - **Timing of 1 second** corresponds to Bit 0.
   - Similar to the sender, the receiver sleeps for the duration of the received timing information to simulate the reception process.

4. **Main Class**: This class contains the `main` method to execute the program.

   - Initializes the `TimingConvertChannel`.
   - Creates instances of `Sender` and `Receiver`.
   - Starts the sender and receiver threads.
   - Waits for both threads to complete using `join()`.
## Output

The program will output the sent and received timing information along with the reconstructed binary message, showcasing the operation of the timing covert channel.


# Feistel Algorithm
This is a Feistel algorithm but it is not a classic one, it contains some changes.
The main process of the algorithm in one round is as below:

<p align="center">
  <img src="https://github.com/nawidadkhah/feistelAlgorithm/assets/79360286/8fb158ee-63a1-4964-aad7-867ad0292289">
</p>

# F function 
This function is used for change parts of the string with math operations and help the right part of the string.
Tables help us to change the length of the string.

# New generating sub-keys
In the algorithm, we change how to create sub-keys. we replace it with the s-box table. in each iteration, we create a specific sub-key that inspired by the previous one 
and the first sub-key, permutation duo to the original key.
