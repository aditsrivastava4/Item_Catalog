import React, { Component } from 'react';

class Catalog extends Component {
    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            items: []
        };
        this.getData()
    }

    getData() {
        let data = [];
        fetch('/API/catalog/category.json')
            .then(catalogItem => catalogItem.json())
            .then((result) => {
                result.results.forEach(item => {
                    data.push(item.category)
                });
                this.setState({
                    isLoaded: true,
                    items: data
                })
            })
    }

    render() {
        const { error, isLoaded, items } = this.state;

        if (error) {
            return <div>Error: {error.message}</div>;
        } else if (!isLoaded) {
            return <div>Loading...</div>;
        } else {
            return (
                <div className="container">
                    <div className="row">
                        <div className="col-sm-12 col-md-12 col-lg-12 text-center">
                            <h1>Book Catalog</h1>
                        </div>
                        {
                            items.map((item) => {
                                return (
                                    <div id="bgColor" className="col-sm-4 col-md-4 col-lg-4 text-center category">
                                        <h4 onClick={this.props.ItemClick}>{item}</h4>
                                    </div>
                                )
                            })
                        }
                    </div>
                </div>
            );
        }
    }
}

export default Catalog;