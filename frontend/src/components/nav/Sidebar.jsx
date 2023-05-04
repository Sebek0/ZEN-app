import React from "react";
import Zen from "../../assets/zen.gif";
import PropTypes from "prop-types";


const Sidebar = ({setDisplayedClanmateId}) => {
	const clanmates = [
		{
			id: 1,
			name: "Andones",
			emblem:
				"https://www.bungie.net/common/destiny2_content/icons/a89532752a40cec06120292c3e3ba3ff.jpg",
		},
		{
			id: 2,
			name: "Filip",
			emblem:
				"https://www.bungie.net/common/destiny2_content/icons/a89532752a40cec06120292c3e3ba3ff.jpg",
		},
		{
			id: 3,
			name: "Sebek",
			emblem:
				"https://www.bungie.net/common/destiny2_content/icons/a89532752a40cec06120292c3e3ba3ff.jpg",
		},
	];

	return (
		<div className='bg-secondary w-full lg:min-w-[22rem] lg:w-[22rem] lg:mr-5'>
			<div className=' w-10/12 h-1/6 flex align-middle flex-shrink-0 mx-auto my-2'>
				<div className='text-gray-500 mx-auto my-auto p-3 bg-primary/50 rounded-lg flex flex-row'>
					<img
						src={Zen}
						alt='Zen'
						width={50}
						height={50}
						className='mx-auto my-auto rounded-lg'></img>
					<input
						className=' ml-5 text-white bg-transparent appearance-none focus:outline-0'
						placeholder='...?'></input>
				</div>
			</div>
			<div className=' h-4/6 flex align-middle'>
				<div className='text-gray-500 w-full lg:w-10/12 mx-auto h-full my-auto bg-primary/50 rounded-lg overflow-y-auto'>
					{clanmates.map((clanmate) => (
						<div
							className='mx-auto my-5 flex flex-row rounded-md p-4 lg:p-2 hover:cursor-pointer hover:shadow-lg transition duration-500 ease-in-out transform hover:-translate-y-1 hover:scale-101  w-[28rem] lg:w-11/12'
							key={clanmate.id}
							onClick={() => setDisplayedClanmateId(clanmate.id)}>
							<img
								src={clanmate.emblem}
								alt='Zen'
								width={50}
								height={50}
								className='mx-auto my-auto rounded-lg'></img>

							<div className='text-white text-lg w-9/12'>
								<p>{clanmate.name}</p>
								<strong className='text-xs text-purple-600 drop-shadow-lg tracking-tighter'>
									Reckoner
								</strong>
							</div>
						</div>
					))}
				</div>
			</div>
			<footer className=' h-1/6 hidden lg:flex align-middle'>
				<div className='text-white w-10/12 mx-auto h-1/4 my-auto bg-primary/50 rounded-lg '>
					<div className='flex text-xs align-baseline'>
						<p className='mx-auto pt-3 flex flex-row'>
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
};


export default Sidebar;
