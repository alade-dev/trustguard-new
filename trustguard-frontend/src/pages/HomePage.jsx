import { useEffect, useState } from "react";
import { motion } from "framer-motion";

import AiLogo from "../assets/ai-logo.png";
import Aibg from "../assets/ai-bg.webp";

import { useNavigate } from "react-router-dom";
import { web3Auth } from "@/hooks/Wallet";

function HomePage() {
  const [, setProvider] = useState(null);
  const [loggedIn, setLoggedIn] = useState(false);

  const [loading, setLoading] = useState(true);

  // console.log(userInfo.profileImage);

  const navigate = useNavigate();

  const handleGetStarted = () => {
    navigate("/upload");
  };

  useEffect(() => {
    const init = async () => {
      try {
        await web3Auth.initModal();
        setProvider(web3Auth.provider);

        if (web3Auth.connected) {
          setLoggedIn(true);
        }
      } catch (error) {
        console.error("Error Initializing Web3Auth", error);
      } finally {
        setLoading(false);
      }
    };
    init();
    const handleConnected = async () => {
      setLoggedIn(true);
      setProvider(web3Auth.provider);
    };

    const handleDisconnected = () => {
      setLoggedIn(false);
      setProvider(null);
    };

    web3Auth.on("connected", handleConnected);
    web3Auth.on("disconnected", handleDisconnected);

    return () => {
      web3Auth.off("connected", handleConnected);
      web3Auth.off("disconnected", handleDisconnected);
    };
  }, []);

  const login = async () => {
    if (!web3Auth) {
      console.error("Web3Auth is not initialized");
      return;
    }
    try {
      const web3authProvider = await web3Auth.connect();
      setProvider(web3authProvider);
      setLoggedIn(true);
    } catch (error) {
      console.error(error);
    }
  };

  if (loading) {
    return (
      <div className="absolute  -translate-x-1/2 -translate-y-1/2 top-1/2 left-1/2">
        <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-blue-500"></div>
        <h1></h1>
      </div>
    );
  }

  return (
    <div
      className="min-h-screen md:pt-8 text-white px-8 bg-cover bg-no-repeat bg-center relative"
      style={{ backgroundImage: `url(${Aibg})` }}
    >
      <div className="absolute top-0 left-0 w-full h-full bg-black/70 z-0"></div>
      <main className="flex flex-col justify-center items-center space-y-16 mt-20 z-10 relative">
        <div className=" mx-auto max-w-7xl justify-center grid items-center md:grid-cols-2 gap-28 ">
          <div className="space-y-9">
            <motion.h1
              className="text-5xl font-semibold shadow-lg leading-normal text-start"
              initial={{ opacity: 0, y: -50 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
            >
              AI-Powered Audit and Reputation Security
            </motion.h1>
            <p className="text-xl text-gray-400 text-start max-w-2xl">
              Revolutionizing Smart Contract Verification. Safeguard smart
              contracts across all chains—Ethereum, Avalanche, Solana, Arbitrum,
              and more.
            </p>
          </div>

          <motion.img
            src={AiLogo}
            alt="AI Bot"
            className="h-fit w-fit lg:ml-16  object-contain"
            animate={{ y: [0, -10, 0] }}
            transition={{ repeat: Infinity, duration: 2, ease: "easeInOut" }}
          />
        </div>
        {!loggedIn ? (
          <button
            onClick={login}
            className="px-6 py-3  bg-blue-600 rounded-3xl hover:bg-blue-500 text-lg"
          >
            Login
          </button>
        ) : (
          <button
            onClick={handleGetStarted}
            className="px-6 py-3  bg-blue-600 rounded-3xl hover:bg-blue-500 shadow-2xl text-lg"
          >
            Get Started
          </button>
        )}
      </main>
    </div>
  );
}

export default HomePage;
