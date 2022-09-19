import React, {Component} from 'react';
import Box from '@mui/material/Box';
import Tab from '@mui/material/Tab';
import TabContext from '@mui/lab/TabContext';
import TabList from '@mui/lab/TabList';
import TabPanel from '@mui/lab/TabPanel';
import Classification from '../classification';
import Data from '../data';
import { Image } from 'mui-image'

export default class Home extends Component {
    constructor(props){
        super(props);
        this.state ={
            value: "1"
        }
        this.handleChange = this.handleChange.bind(this)
    }
    handleChange = (event, newValue) => {
        this.setState({value: newValue});
    }
    render () {  return (
        <Box sx={{ width: '70%', typography: 'body1', margin: "0 auto"}}>
          <TabContext value={this.state.value}>
            <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
              <TabList onChange={this.handleChange} aria-label="lab API tabs example">
                <Tab label="Classification" value="1" />
                <Tab label="Data" value="2" />
                <Tab label="Graph" value="3" />
              </TabList>
            </Box>
            <TabPanel value="1"><Classification/></TabPanel>
            <TabPanel value="2"><Data/></TabPanel>
            <TabPanel value="3"><Image src="static/content/out_trained_full_30.png"/></TabPanel>
          </TabContext>
        </Box>
      );
    }
}