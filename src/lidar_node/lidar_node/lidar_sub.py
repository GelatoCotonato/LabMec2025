import gz.transport as transport
import gz.msgs as msgs

# topic su cui pubblicare i comandi
topic_pub = "/cmd_vel"
# topic da cui leggere i dati LIDAR (modifica se serve)
topic_sub = "/lidar_topic"

node = transport.Node()

pub = node.advertise(topic_pub, msgs.Twist)

def callback(msg):
    # msg è un messaggio di tipo LaserScan
    # Controlla se tutte le distanze sono > 1.0
    all_more = all(r > 1.0 for r in msg.ranges)

    cmd = msgs.Twist()
    if all_more:
        cmd.linear.x = 0.5
        cmd.angular.z = 0.0
    else:
        cmd.linear.x = 0.0
        cmd.angular.z = 0.5

    pub.publish(cmd)

node.subscribe(topic_sub, callback)

print(f"Subscribed to {topic_sub}, publishing commands on {topic_pub}")

try:
    transport.wait_for_shutdown()
except KeyboardInterrupt:
    print("Shutting down")