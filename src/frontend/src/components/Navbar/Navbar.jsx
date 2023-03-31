import React, { useEffect, useState } from "react";

import { GiHamburgerMenu } from "react-icons/gi";
import { Link } from "react-router-dom";
import { useAuthModal } from "../../context/sheContext";

import "./Navbar.css";
import app_logo from "../../assets/navbar/Ark.jpg";

const Navbar = () => {
    const { setopenauthmodal, setisuser, setisuserreg } = useAuthModal();

    return (
        <>
            <div className="navbar_main_parent sticky-top">
                <div className="navbar_subparent">
                    <Link to="/" className="navbar_brand tracking-[0.2rem]">
                        <img src={app_logo} alt="navlogo" />
                    </Link>

                    <div className="navbar_linksdiv gap-1">
                        <Link to="/" className="navbar_links">
                            Home
                        </Link>

                        <Link to="/about" className="navbar_links">
                            About Us
                        </Link>
                        <Link to="/service" className="navbar_links">
                            Service
                        </Link>

                        <Link to="/contact" className="navbar_links">
                            Contact
                        </Link>
                    </div>

                    <div className="navbar_btndiv gap-2">
                        <button
                            type="button"
                            className=" navbar_login_button btn"
                            onClick={() => {
                                setopenauthmodal(true);
                                document.body.classList.add("fixed");
                                setisuserreg(false);
                            }}
                        >
                            Login
                        </button>
                        <button
                            type="button"
                            className=" navbar_joinus_button btn"
                            onClick={() => {
                                setopenauthmodal(true);
                                document.body.classList.add("fixed");
                                setisuserreg(true);
                            }}
                        >
                            Sign up
                        </button>
                    </div>
                </div>
            </div>
        </>
    );
};

export default Navbar;
