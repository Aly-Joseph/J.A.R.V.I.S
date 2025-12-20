import { AccessToken } from "livekit-server-sdk";
import express from "express";

const app = express();

app.get("/token", (req, res) => {
  const room = "jarvis-room";
  const identity = "jarvis-user";

  const token = new AccessToken(
    process.env.LIVEKIT_API_KEY,
    process.env.LIVEKIT_API_SECRET,
    { identity }
  );

  token.addGrant({ roomJoin: true, room });
  res.json({ token: token.toJwt() });
});

app.listen(3000, () => console.log("Token server running"));
