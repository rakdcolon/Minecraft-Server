# Use the itzg/minecraft-server image as the base image
FROM itzg/minecraft-server

# (Optional) Expose the default Minecraft port
EXPOSE 25565

# (Optional) Set default environment variables.
# You can override these when running the container.
ENV EULA=TRUE

# Declare /data as a volume (for persistent server data)
VOLUME ["/data"]

# (Optional) Copy additional configuration files if necessary
# COPY server.properties /data/

# The base image already defines the CMD to start the server,
# so no additional CMD is needed here.
