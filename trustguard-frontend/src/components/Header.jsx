import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "../components/ui/dropdown-menu";
import { ChevronDown, LogIn } from "lucide-react";
import { Button } from "../components/ui/button";
import { useEffect, useState } from "react";
import { web3Auth } from "@/hooks/Wallet";
import { Link, NavLink } from "react-router-dom";

const Header = () => {
  const [, setProvider] = useState(null);
  const [loggedIn, setLoggedIn] = useState(false);
  const [userInfo, setUserInfo] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const init = async () => {
      try {
        await web3Auth.initModal();

        if (web3Auth.connected) {
          setProvider(web3Auth.provider);
          setLoggedIn(true);
          const user = await web3Auth.getUserInfo();
          setUserInfo(user);
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
      const user = await web3Auth.getUserInfo();
      setUserInfo(user);
    };

    const handleDisconnected = () => {
      setLoggedIn(false);
      setProvider(null);
      setUserInfo(null);
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
      const user = await web3Auth.getUserInfo();
      setUserInfo(user);
    } catch (error) {
      console.error("Error during login:", error);
    }
  };

  const logout = async () => {
    if (!web3Auth) {
      console.error("Web3Auth is not initialized");
      return;
    }
    try {
      await web3Auth.logout();
      setProvider(null);
      setLoggedIn(false);
      setUserInfo(null);
    } catch (error) {
      console.error("Error during logout:", error);
    }
  };

  const getUserInfo = async () => {
    if (web3Auth.connected) {
      try {
        const user = await web3Auth.getUserInfo();
        setUserInfo(user);
      } catch (error) {
        console.error("Error getting user info:", error);
      }
    }
  };

  if (loading) {
    return (
      <div className="absolute -translate-x-1/2 -translate-y-1/2 top-1/2 left-1/2">
        <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <header className="md:mx-auto w-full md:max-w-7xl justify-around flex md:justify-between items-center md:px-10 border-gray-700 md:border rounded-full py-6">
      <Link to={""}>
        <h1 className="text-xl md:text-3xl font-bold">TrustGuard</h1>
      </Link>

      <ul className="hidden font-semibold md:flex gap-5">
        <li>
          <NavLink
            to={"/faq"}
            className={({ isActive }) => (isActive ? "text-blue-500" : "")}
          >
            FAQ
          </NavLink>
        </li>
        <li>
          <NavLink
            to={"/how-it-works"}
            className={({ isActive }) => (isActive ? "text-blue-500" : "")}
          >
            How it works
          </NavLink>
        </li>
        <li>
          <NavLink
            to={"/about"}
            className={({ isActive }) => (isActive ? "text-blue-500" : "")}
          >
            About
          </NavLink>
        </li>
      </ul>

      {!loggedIn ? (
        <Button
          onClick={login}
          className="px-4 py-2 lg:px-8 lg:py-6 bg-blue-600 rounded-3xl hover:bg-blue-500 text-white font-medium text-base md:text-xl"
        >
          Login
          <LogIn className="ml-1 md:ml-2 h-4 w-4 md:h-5 md:w-5" />
        </Button>
      ) : (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button
              variant="ghost"
              size="icon"
              className="flex items-center shadow-2xl cursor-pointer"
            >
              <img
                src={
                  userInfo && userInfo.profileImage
                    ? userInfo.profileImage
                    : "https://avatars.dicebear.com/api/avataaars/anonymous.svg"
                }
                alt="User profile"
                className="h-10 w-10 rounded-full object-cover mr-1"
              />
              <ChevronDown className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem onClick={getUserInfo}>
              {userInfo ? userInfo.name : "Profile"}
            </DropdownMenuItem>
            <DropdownMenuItem>
              <a href="/settings">Settings</a>
            </DropdownMenuItem>
            <DropdownMenuItem onClick={logout}>Sign Out</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      )}
    </header>
  );
};

export default Header;
