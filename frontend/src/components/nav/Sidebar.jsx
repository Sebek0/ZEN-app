import axios from "axios";
import PropTypes from "prop-types";
import React from "react";
import { useQuery } from "react-query";
import Zen from "../../assets/zen.gif";
import { BUNGIE_URL } from "../../const/BungieUrl";

/**
 * Sidebar component
 * @param {*} setDisplayedClanmateId - function that sets displayedClanmateId in App.jsx
 * @returns Sidebar component
 */
const Sidebar = ({ setDisplayedClanmateId, displayedId }) => {
	const { isLoading, isError, data, error } = useQuery(["clanmates"], () =>
		axios.get("http://127.0.0.1:8000/api/v1/guardians/clanmates/").then((res) => res.data)
	);

	const [searchValue, setSearchValue] = React.useState("");
	const [filteredClanmates, setFilteredClanmates] = React.useState([]);

	React.useEffect(() => {
		if (data) {
			if (searchValue === "") {
				setFilteredClanmates(data);
			} else {
				const filtered = data.filter((clanmate) =>
					clanmate.name.toLowerCase().includes(searchValue.toLowerCase())
				);
				setFilteredClanmates(filtered);
			}
		}
	}, [data, searchValue]);

	const handleSearch = (e) => {
		setSearchValue(e.target.value);
	};

	return (
		<div className='bg-secondary w-full lg:min-w-[22rem] lg:w-[22rem] shadow-lg rounded-lg'>
			<div className=' w-10/12 lg:h-1/6 flex align-middle flex-shrink-0 mx-auto my-2'>
				<div className='text-gray-500 mx-auto my-auto p-3 bg-primary/50 rounded-lg flex flex-row'>
					<img
						src={Zen}
						alt='Zen'
						width={50}
						height={50}
						className='mx-auto my-auto rounded-lg'></img>
					<input
						className=' ml-5 text-white bg-transparent appearance-none focus:outline-0'
						onChange={handleSearch}
						placeholder='...?'></input>
				</div>
			</div>
			<div className='h-96 lg:h-4/6 flex align-middle mt-5'>
				<div className='text-gray-500 w-full lg:w-10/12 mx-auto h-full my-auto bg-primary/50 rounded-lg overflow-x-hidden overflow-y-auto'>
					{isLoading && (
						<div className='flex flex-col mx-auto'>
							<span className='text-white text-md text-center my-5'>Loading...</span>
						</div>
					)}
					{isError && <p>Error: {error.message}</p>}
					{!isLoading &&
						!isError &&
						filteredClanmates.map((clanmate) => (
							<div
								className={`mx-auto opacity-0 my-5 flex flex-row rounded-md p-4 lg:p-2 hover:cursor-pointer hover:shadow-lg transition duration-500 ease-in-out transform hover:-translate-y-1 hover:scale-101 w-[28rem] lg:w-11/12 appear ${
									displayedId === clanmate.guardian_id ? "bg-secondary/50" : ""
								}`}
								style={{
									animationDelay: `${clanmate.guardian_id * 0.1}s`,
								}}
								key={clanmate.guardian_id}
								onClick={() => setDisplayedClanmateId(clanmate.guardian_id)}>
								<img
									src={BUNGIE_URL + clanmate.characters_info[0].char_emblem_path}
									alt='Zen'
									width={50}
									height={50}
									className='mx-auto my-auto rounded-lg'></img>

								<div className='text-white text-lg w-9/12'>
									<p>{clanmate.name}</p>
									<strong className='text-xs text-purple-600 drop-shadow-lg tracking-tighter'>
										{clanmate.characters_info[0].title}
									</strong>
								</div>
							</div>
						))}
				</div>
			</div>
			<footer className='hidden lg:flex align-middle mt-5'>
				<div className='text-white w-10/12 mx-auto h-1/4 my-auto bg-primary/50 rounded-lg '>
					<div className='flex text-xs align-baseline'>
						<p className='mx-auto p-3 flex flex-row'>
							Made by Andones, Filip, Sebek <span className='text-md pl-2'> ❤️</span>
						</p>
					</div>
				</div>
			</footer>
		</div>
	);
};

Sidebar.propTypes = {
	setDisplayedClanmateId: PropTypes.func.isRequired,
	displayedId: PropTypes.number.isRequired,
};

export default Sidebar;
