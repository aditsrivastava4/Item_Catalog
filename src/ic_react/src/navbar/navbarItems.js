import React, { Component } from 'react';
import Cookies from 'js-cookie'

class NavbarItem extends Component {
    constructor(props) {
        super(props);
        this.state = {
            loggedIn: Cookies.get('loggedIn'),
            username: Cookies.get('username')
        };
    }
    logout()
    {
        fetch('/logout')
        .then((logoutStatus) => {
            return logoutStatus.json()
        })
        .then((status) => {
            if(status.logout) {
                Cookies.remove('username')
                Cookies.remove('type')
                Cookies.remove('loggedIn')
                Cookies.remove('uid')
                setTimeout(function() {
                    window.location.href = "/";
                }, 500);
            }
        })
    }
    render() {
        const { loggedIn, username } = this.state
        let signup = !loggedIn ? <li><a href="/signup"><span className= "glyphicon glyphicon-user"></span> Sign Up</a></li> : ""
        let logIcon
        if( !loggedIn ) {
            logIcon = <li><a href="/login"><span className="glyphicon glyphicon-log-in"></span> Login</a></li>
        } else {
            logIcon = <li><a className="pointer" onClick={ this.logout }><span className="glyphicon glyphicon-log-out"></span> Logout</a></li>
        }

        return (
            <div id="navbar" className="navbar-collapse collapse">
                <ul className="nav navbar-nav navbar-right paddingul">
                    <li><a href="/API-doc">API</a></li>
                    {signup}
                    {logIcon}
                </ul>
            </div>
        );
    }
}

export default NavbarItem;
