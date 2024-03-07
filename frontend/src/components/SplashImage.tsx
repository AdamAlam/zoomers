"use client";
import { useState, useEffect } from "react";
import "./SplashImage.css";

interface Props {}
const SplashImage = (props: Props) => {
  const duneId = "693134";
  const bearer = process.env.TMDB_BEARER;
  const [backgroundImg, setBackground] = useState("");
  const imageBaseUrl = "https://image.tmdb.org/t/p/original";

  useEffect(() => {
    fetch(`https://api.themoviedb.org/3/movie/${duneId}/images`, {
      headers: {
        accept: "application/json",
        Authorization: `Bearer ${bearer}`,
      },
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error(`API call failed with status: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        if (data.backdrops && data.backdrops.length > 0) {
          setBackground(data.backdrops[0].file_path);
        } else {
          console.error("No backdrops available");
        }
      })
      .catch((error) => console.error("Fetching error:", error));
  }, [bearer]);

  console.log(`Background Image URL: ${imageBaseUrl}${backgroundImg}`); //
  return (
    <header
      className="bg-cover"
      style={{
        backgroundImage: `url(${imageBaseUrl}${backgroundImg})`,
        height: "700px",
      }}
    >
      <div id="banner-fade-bottom" />
    </header>
  );
};
export default SplashImage;
