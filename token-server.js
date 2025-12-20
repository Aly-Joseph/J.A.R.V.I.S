import express from "express";
import dotenv from "dotenv";
import { AccessToken } from "livekit-server-sdk";

dotenv.config();
const app = express();

app.get("/token", (req, res) => {
  const room = "jarvis-room";
  const identity = "user-" + Math.random().toString(36).slice(2);

  const token = new AccessToken(
    process.env.LIVEKIT_API_KEY,
    process.env.LIVEKIT_API_SECRET,
    { identity }
  );

  token.addGrant({ roomJoin: true, room });
  res.json({ token: token.toJwt(), url: process.env.LIVEKIT_URL });
});

app.listen(3000, () =>
  console.log("✅ LiveKit token server running on http://localhost:3000")
);
