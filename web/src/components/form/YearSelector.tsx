import { useRecoilState } from 'recoil';
import React, { ChangeEvent } from 'react';
import { Select } from '@chakra-ui/react';
import { predictionYear, predictionYearError } from '../../state/atoms';

const YearSelector = () => {
  const [yearValue, setYearValue] = useRecoilState(predictionYear);
  const [isError, setIsError] = useRecoilState(predictionYearError);

  const selectYear = (e: ChangeEvent<HTMLSelectElement>) => {
    setYearValue(+e.target.value);

    if (isError) {
      setIsError(+e.target.value === 0);
    }
  };
  return (
    <Select
      placeholder="Select year"
      id="year"
      value={yearValue}
      onChange={selectYear}
      _focus={{
        borderColor: 'blue.500',
      }}
    >
      <option value="2008">2008</option>
      <option value="2009">2009</option>
      <option value="2010">2010</option>
      <option value="2011">2011</option>
      <option value="2012">2012</option>
      <option value="2013">2013</option>
      <option value="2014">2014</option>
      <option value="2015">2015</option>
    </Select>
  );
};

export default YearSelector;
