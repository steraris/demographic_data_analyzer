import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df['race'].value_counts()

    # What is the average age of men?
    sex = df['sex'].value_counts()
    men = df.loc[df['sex'] == 'Male', 'age']
    
    average_age_men = round((df.loc[df['sex'] == 'Male', 'age'].mean()),1)

    # What is the percentage of people who have a Bachelor's degree?
    education_counts = df['education'].value_counts()
    percentage_bachelors = round((education_counts['Bachelors']/education_counts.sum())*100,1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?
    edu_salary = df.groupby(['education','salary'])['salary'].count()
    

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = edu_salary[['Bachelors','Masters','Doctorate']].sum()
    lower_education = edu_salary[['10th','11th','12th','1st-4th','5th-6th','7th-8th','9th','Assoc-acdm','Assoc-voc','HS-grad','Preschool','Prof-school','Some-college']].sum()

    # percentage with salary >50K
    high_edu_total = edu_salary[['Bachelors','Masters','Doctorate']].sum()
    high_ed_sal_more_50k = edu_salary['Bachelors']['>50K'] + edu_salary['Masters']['>50K'] + edu_salary['Doctorate']['>50K']
    

    higher_education_rich = round((high_ed_sal_more_50k / high_edu_total) * 100,1)
    low_edu_salary = edu_salary.drop(['Bachelors','Masters','Doctorate'])
    low_edu_total = low_edu_salary.sum()
    low_ed_sal_more_50K = (low_edu_salary.groupby(['salary']).sum())['>50K']
    lower_education_rich = round((low_ed_sal_more_50K / low_edu_total) * 100,1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = round(df['hours-per-week'].min(),1)

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    hpw_salary = df[['hours-per-week','salary']]
    hpw_sal_grouped = hpw_salary.groupby(['hours-per-week','salary'])['salary'].count()
    
    
    num_min_workers = hpw_sal_grouped[1]['>50K']

    rich_percentage = round((hpw_sal_grouped[1]['>50K'] / hpw_sal_grouped[1].sum()) * 100,1)

    # What country has the highest percentage of people that earn >50K?
    rich_pop_by_country = df.loc[df['salary'] == '>50K', 'native-country'].value_counts()
    country_pop = df['native-country'].value_counts()
    rich_percent = (rich_pop_by_country / country_pop) * 100
    highest_earning_country = rich_percent.idxmax()
    highest_earning_country_percentage = round(rich_percent.max(),1)

    # Identify the most popular occupation for those who earn >50K in India.
    india = df['native-country'] == 'India'
    india_rich = df.loc[india & (df['salary'] == '>50K'),'occupation'].value_counts()
    top_IN_occupation = india_rich.idxmax()

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
