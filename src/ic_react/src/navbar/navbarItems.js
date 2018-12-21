import React, { Component } from 'react';

class NavbarItem extends Component {
    render() {
        return (
            <div id="navbar" className="navbar-collapse collapse">
                <ul className="nav navbar-nav navbar-right paddingul">
                    <li><a href="/API-doc">API</a></li>
                    <li><a href="/signup"><span className="glyphicon glyphicon-user"></span> Sign Up</a></li>
                    <li><a href="/login"><span className="glyphicon glyphicon-log-in"></span> Login</a></li>
                </ul>
            </div>
        );
    }
}

export default NavbarItem;
