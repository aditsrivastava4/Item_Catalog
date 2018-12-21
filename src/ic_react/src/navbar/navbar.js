import React, { Component } from 'react';
import NavbarItem from './navbarItems'
import NavbarHeader from './navbar_header'

class Navbar extends Component {
    render() {
        return (
            <div className="container-fluid">
            <nav className="navbar navbar-default">
                <div className="container-fluid">
                    <NavbarHeader />
                    <NavbarItem />
                </div>
            </nav>
        </div>
        );
    }
}

export default Navbar;
