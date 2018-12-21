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

    itemEvent(event) {
        console.log(event.currentTarget)
        alert(event)
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
                        <div className="col-md-2"></div>
                        <div className="col-md-8">
                            {
                                items.map((d) => {
                                    return <h1 onClick={this.itemEvent}>{d}</h1>
                                })
                            }
                        </div>
                        <div className="col-md-2"></div>
                    </div>
                </div>
            );
        }
    }
}

export default Catalog;