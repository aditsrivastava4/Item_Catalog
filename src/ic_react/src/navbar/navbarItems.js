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
    checkLoggedIn()
    {
        this.setState({
            loggedIn: Cookies.get('loggedIn'),
            username: Cookies.get('username')
        })
    }
    render() {
        const { loggedIn, username } = this.state
        const signup = !loggedIn ? <li><a href="/signup"><span className= "glyphicon glyphicon-user"></span> Sign Up</a></li> : ""
        const logIcon = !loggedIn ? <li><a href="/login"><span className="glyphicon glyphicon-log-in"></span> Login</a></li> : <li><a href="/logout"><span className="glyphicon glyphicon-log-in"></span> Logout</a></li>

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
