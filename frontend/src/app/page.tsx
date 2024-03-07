"use client";
import Navbar from "@/components/Navbar";
import SplashImage from "@/components/SplashImage";
import { useEffect, useState } from "react";

export default function Home() {
  return (
    <div className="flex flex-col container">
      <Navbar />
      <SplashImage />
    </div>
  );
}
