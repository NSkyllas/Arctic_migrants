import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import xarray as xr
import numpy as np
import hvplot.xarray
import hvplot
import holoviews as hv
import holoviews.plotting.mpl
import base64

# In[2]:

st.set_page_config(
     #page_title="CMIP6 climate variables",
     #layout="wide",
     initial_sidebar_state="expanded",
      )



st.sidebar.title('Arctic migrants consortium climate data')

st.sidebar.markdown('**Welcome to the CMIP6 climate variables interactive guide! Below, you can select whether you want to see all the available variables, filter them or see a NetCDF file example:**')
tabletype = st.sidebar.radio('', ['Search CMIP6 variables', 'Filter CMIP6 variables', 'Delivered variables', 'Interactive plots'])


dict1 = pd.read_excel('CMIP6_MIP_tables.xlsx', sheet_name = None)

@st.cache
def load_data():
    df = pd.concat(dict1.values(), ignore_index=True)
    return df[['Long name', 'units', 'description', 'comment', 'Variable Name', 'CF Standard Name', 'dimensions', 'modeling_realm', 'frequency', 'MIPs (by experiment)']]
    
data = load_data()

if tabletype == 'Search CMIP6 variables':
	st.title('Search CMIP6 variables')
	terms = st.text_input('Search').lower().split()
	if len(terms) == 0:
		st.write(data)
		st.write('You have ') 	
		st.write(len(data))
		st.write('variables!')
		col1, col2 = st.beta_columns(2)	
		with col1:
			fig1= plt.figure(figsize=(5, 4))
			sns.countplot(y=data['modeling_realm'], order = data['modeling_realm'].value_counts().index)
			st.pyplot(fig1)
	
		with col2:
			fig2= plt.figure(figsize=(5, 4))
			sns.countplot(y=data['frequency'], order = data['frequency'].value_counts().index)
			st.pyplot(fig2)
	
	elif len(terms) == 1:
		df1 = data[data['Long name'].str.lower().str.contains(terms[0])]
		st.write(df1)
		st.write('You have ') 	
		st.write(len(df1))
		st.write('variables!')
		
		col1, col2 = st.beta_columns(2)	
		with col1:
			fig1= plt.figure(figsize=(5, 4))
			sns.countplot(y=data[data['Long name'].str.lower().str.contains(terms[0])]['modeling_realm'], order = data[data['Long name'].str.lower().str.contains(terms[0])]['modeling_realm'].value_counts().index)
			st.pyplot(fig1)
	
		with col2:
			fig2= plt.figure(figsize=(5, 4))
			sns.countplot(y=data[data['Long name'].str.lower().str.contains(terms[0])]['frequency'], order = data[data['Long name'].str.lower().str.contains(terms[0])]['frequency'].value_counts().index)
			st.pyplot(fig2)
		
		##########################
		csv = df1.to_csv(index=False)
		b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
		href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as &lt;some_name&gt;.csv)'
		st.markdown("## Download the table:")
		st.markdown(href, unsafe_allow_html=True)	
		###########################
		
			
	else:
		search, search2 = terms
		df2 = data[(data['Long name'].str.lower().str.contains(search)) & (data['Long name'].str.lower().str.contains(search2))]
		st.write(df2)
		st.write('You have ') 	
		st.write(len(df2))
		st.write('variables!')
		
		col1, col2 = st.beta_columns(2)	
		with col1:
			fig1= plt.figure(figsize=(5, 4))
			sns.countplot(y=data[(data['Long name'].str.lower().str.contains(search)) & (data['Long name'].str.lower().str.contains(search2))]['modeling_realm'], order = data[(data['Long name'].str.lower().str.contains(search)) & (data['Long name'].str.lower().str.contains(search2))]['modeling_realm'].value_counts().index)
			st.pyplot(fig1)
	
		with col2:
			fig2= plt.figure(figsize=(5, 4))
			sns.countplot(y=data[(data['Long name'].str.lower().str.contains(search)) & (data['Long name'].str.lower().str.contains(search2))]['frequency'], order = data[(data['Long name'].str.lower().str.contains(search)) & (data['Long name'].str.lower().str.contains(search2))]['frequency'].value_counts().index)
			st.pyplot(fig2)
	
		##########################
		csv = df2.to_csv(index=False)
		b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
		href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as &lt;some_name&gt;.csv)'
		st.markdown("## Download the table:")
		st.markdown(href, unsafe_allow_html=True)	
		###########################
		#
elif tabletype == 'Delivered variables':
	st.title('Delivered variables for the WPs')
#	
	dictdel = pd.read_excel('Delivered_var.xlsx', sheet_name = None)
	@st.cache
	def load_datadel():
		dfdel = pd.concat(dictdel.values(), ignore_index=True)
		return dfdel
	datadel = load_datadel()
	st.write(datadel)
	
	##########################
	csv = datadel.to_csv(index=False)
	b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
	href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as &lt;some_name&gt;.csv)'
	st.markdown("## Download the table:")
	st.markdown(href, unsafe_allow_html=True)	
	###########################
	
elif tabletype == 'Filter CMIP6 variables':
	st.title('Filter CMIP6 variables')	
	st.sidebar.markdown('Please use the 3 available filters to confine your search. Barplots will start appearing and at the end you will see the filtered table.')
	
	realm = st.multiselect('Realm', data['modeling_realm'].unique())
	f_data = data[(data['modeling_realm'].isin(realm))]
	
	freq = st.multiselect('Frequency', f_data['frequency'].unique())
	f_data2 = f_data[(f_data['frequency'].isin(freq))]
	
	dim = st.multiselect('Dimensions', f_data2['dimensions'].unique())
	f_data3 = f_data2[(f_data2['dimensions'].isin(dim))]
	
	if len(realm) > 0:
		col3, col4 = st.beta_columns(2)
		with col3:
			fig3= plt.figure(figsize = (6, len(f_data['dimensions'].unique())*0.2))
			sns.countplot(y=f_data['frequency'], order = f_data['frequency'].value_counts().index)
			st.pyplot(fig3)
	
		if len(freq) > 0:
				
			with col4:
				fig4= plt.figure(figsize = (5, len(f_data2['dimensions'].unique())*0.5))
				sns.countplot(y=f_data2['dimensions'], order = f_data2['dimensions'].value_counts().index)
				st.pyplot(fig4)
			if len(dim) > 0:
				st.subheader('Filtered data')
				st.write('You have ') 	
				st.write(len(f_data3))
				st.write('variables!')
				st.write(f_data3)			
				
				##########################
				csv = f_data3.to_csv(index=False)
				b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
				href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as &lt;some_name&gt;.csv)'
				st.markdown("## Download the table:")
				st.markdown(href, unsafe_allow_html=True)	
				###########################
	else:
		st.subheader('You can start using the filters!')
		
	
else:
	st.title('Interactive plots')
	st.sidebar.markdown('Feel free to play around with the interactive plots (move the slider, zoom in/out, select an area) in order to get a feeling of the time scales and spatio-temporal resolution of the CMIP6 variables. In this specific example, only the monthly averages of 1 variable were used, with a spatial resolution of 1x1 degree and 4 depth levels.')
	@st.cache(hash_funcs={xr.core.dataset.Dataset: id},  allow_output_mutation=True)
	def load_data2():
		dset = xr.open_dataset('soil_temp_5years_regridded.nc')
		return dset
    
	data2 = load_data2()
	col7, col8 = st.beta_columns(2)
	with col7:
		f_time = st.slider('Month', 1, 24, 1)
		st.subheader(data2.time.values[f_time-1])
	with col8:
		f_depth = st.slider('Depth level', 1, 4, 1)
		st.subheader(round(data2.depth.values[f_depth-1], 2))
	
	fig5 = plt.figure(figsize=(8, 0.1))
	plot5 = (data2.tsl.isel(time=f_time-1, depth=f_depth-1)-273.15).hvplot(clim=(-50, 50), cmap='RdYlBu_r')
	#st.write(type(plot5))
	st.bokeh_chart(hv.render(plot5, backend='bokeh'))
	st.pyplot(fig5)
	st.markdown('**Fig.1: Global map of Soil Temperature monthly averages ($^o$C), according to the EC-Earth3 model for the years 1850 to 1851**')
	
	st.markdown("---")
	
	fig6 = plt.figure(figsize=(8, 0.1))
	f_depth2 = st.selectbox('Depth level', [1, 2, 3, 4])
	plot6 = (data2.tsl.isel(depth=f_depth2-1).mean(dim='lon')-273.15).T.hvplot(clim=(-50, 50), cmap='RdYlBu_r')
	st.bokeh_chart(hv.render(plot6, backend='bokeh'))
	st.pyplot(fig6)
	st.markdown('**Fig.2: Zonal means of Soil Temperature monthly averages ($^o$C), according to the EC-Earth3 model for the years 1850 to 1851**')
	
	st.markdown("---")
	col5, col6 = st.beta_columns(2)
	with col5:
		f_lon = st.slider('Longitude', -180, 180, 1) 
	with col6:
		f_lat = st.slider('Latitude', -90, 90, 1)
	fig7 = plt.figure(figsize=(8, 0.1))
	plot7 = (data2.tsl.mean(dim='depth').sel(lon=f_lon, lat=f_lat)-273.15).T.hvplot()
	st.bokeh_chart(hv.render(plot7, backend='bokeh'))
	st.pyplot(fig7)
	st.markdown('**Fig.3: Soil Temperature monthly averages ($^o$C), averaged over depth, according to the EC-Earth3 model for the years 1850 to 1851 for gridcell with coordinates (lon, lat):**')
	st.write(data2.lon.values[f_lon+180]); st.write(data2.lat.values[f_lat+90])

	st.markdown('---')
	
	with st.beta_expander("NetCDF file structure"):
		st.write(data2)
		
	with st.beta_expander("NetCDF file contents"):
		st.write(data2.variables)


