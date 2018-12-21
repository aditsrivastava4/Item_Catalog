import React, { Component } from 'react';

class NavbarHeader extends Component {
    render() {
        return (
            <div className="navbar-header">
                <button
                    type="button"
                    className="navbar-toggle collapsed"
                    data-toggle="collapse"
                    data-target="#navbar"
                    aria-expanded="false"
                    aria-controls="navbar">
                    
                    <span className="sr-only">Toggle navigation</span>
                    <span className="icon-bar"></span>
                    <span className="icon-bar"></span>
                    <span className="icon-bar"></span>
                </button>
                <a className="navbar-brand" href="/"><strong>Book Catalog</strong></a>
            </div>
        );
    }
}

export default NavbarHeader;
