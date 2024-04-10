# custom_tools.py
from crewai_tools import BaseTool

class MeetingNotesParser(BaseTool):
    name: str = "Meeting Notes Parser"
    description: str = "Parses .md meeting files to extract structured information."

    def _run(self, filepath: str) -> dict:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.readlines()
        
        extracted_info = {
            "date": "",
            "project": "",
            "participants": [],
            "discussion_points": [],
            "decisions_made": [],
            "action_items": [],
            "external_links": []
        }
        
        current_section = None
        for line in content:
            if line.startswith('## '):
                current_section = line.strip().lower()
            elif current_section == '## meeting details':
                if line.startswith('-[**Date**::'):
                    extracted_info["date"] = line.split(':: ')[1].strip(']\n')
                elif line.startswith('- [**Project**::'):
                    extracted_info["project"] = line.split(':: ')[1].strip('[]\n')
            elif current_section == '## action items':
                if line.startswith('- [ ]'):
                    extracted_info["action_items"].append(line.strip('- [ ] \n'))
            # Implement parsing logic for other sections as needed
        
        return extracted_info


class ProjectInfoParser(BaseTool):
    name: str = "Project Info Parser"
    description: str = "Extracts structured information from project .md files."

    def _run(self, filepath: str) -> dict:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.readlines()
        
        extracted_info = {
            "start_date": "",
            "end_date": "",
            "status": "",
            "project_lead": "",
            "goals": [],
            "links": [],
        }
        
        current_section = None
        for line in content:
            if line.startswith('## '):
                current_section = line.strip().lower()
            elif current_section == '## project overview':
                if line.startswith('- **Start Date**'):
                    extracted_info["start_date"] = line.split('**: ')[1].strip()
                elif line.startswith('- **End Date**'):
                    extracted_info["end_date"] = line.split('**: ')[1].strip()
                elif line.startswith('- **Status**'):
                    extracted_info["status"] = line.split('**: ')[1].strip()
                elif line.startswith('- **Project Lead**'):
                    extracted_info["project_lead"] = line.split('**: ')[1].strip()
            elif current_section == '## project goals':
                if line.startswith('- Goal'):
                    extracted_info["goals"].append(line.strip('- \n'))
            elif line.startswith('https://'):
                extracted_info["links"].append(line.strip())

        return extracted_info
