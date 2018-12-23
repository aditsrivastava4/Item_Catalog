import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import Login from './login_signup/login_index'
import * as serviceWorker from './serviceWorker';
import { Route, Link, BrowserRouter as Router, Switch } from 'react-router-dom'
import SignUp from './login_signup/signup';

const routing = (
    <Router>
        <Switch>
            <Route exact path="/" component={App} />
            <Route exact path="/login" component={Login} />
            <Route exact path="/signup" component={SignUp} />
        </Switch>
    </Router>
)


ReactDOM.render(routing, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: http://bit.ly/CRA-PWA
serviceWorker.unregister();
