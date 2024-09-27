import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;
import java.time.LocalTime;

class TimingConvertChannel {
    private BlockingQueue<Integer> channel;

    public TimingConvertChannel() {
        this.channel = new ArrayBlockingQueue<>(1); // Channel size is 1 for simplicity
    }

    public void send(int timingInfo) throws InterruptedException {
        channel.put(timingInfo);
    }

    public int receive() throws InterruptedException {
        return channel.take();
    }
}

class Sender implements Runnable {
    private TimingConvertChannel channel;

    public Sender(TimingConvertChannel channel) {
        this.channel = channel;
    }

    @Override
    public void run() {
        try {
            String message = "1010"; // Binary message to send
            for (int i = 0; i < message.length(); i++) {
                int bit = Integer.parseInt(String.valueOf(message.charAt(i)));
                int timingInfo = bit == 1 ? 2 : 1; // Different transmission time for bit 1 and bit 0
                channel.send(timingInfo);
                System.out.println(LocalTime.now() + " - Sender: Sent timing info " + timingInfo + " for bit " + bit);
                Thread.sleep(timingInfo * 1000); // Simulate transmission time
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            System.err.println("Sender interrupted");
        }
    }
}

class Receiver implements Runnable {
    private TimingConvertChannel channel;

    public Receiver(TimingConvertChannel channel) {
        this.channel = channel;
    }

    @Override
    public void run() {
        try {
            String receivedMessage = "";
            for (int i = 0; i < 4; i++) { // Assuming 4 bits are being sent
                int receivedTiming = channel.receive();
                int receivedBit = receivedTiming == 2 ? 1 : 0; // Assuming transmission time 2 corresponds to bit 1, and 1 to bit 0
                receivedMessage += receivedBit;
                System.out.println(LocalTime.now() + " - Receiver: Received timing info " + receivedTiming + " for bit " + receivedBit);
                Thread.sleep(receivedTiming * 1000); // Simulate transmission time
            }
            System.out.println("Received message: " + receivedMessage);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            System.err.println("Receiver interrupted");
        }
    }
}

public class main {
    public static void main(String[] args) {
        TimingConvertChannel channel = new TimingConvertChannel();

        Sender sender = new Sender(channel);
        Receiver receiver = new Receiver(channel);

        Thread senderThread = new Thread(sender);
        Thread receiverThread = new Thread(receiver);

        senderThread.start();
        receiverThread.start();

        try {
            senderThread.join();
            receiverThread.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            System.err.println("Main thread interrupted");
        }
    }
}
