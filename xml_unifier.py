#!/usr/bin/env python3
"""
XML Unifier - Programa para unificar múltiplos arquivos XML em um único arquivo
"""

import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class XMLUnifier:
    def __init__(self, input_dir="files", output_file="output/final_list.xml"):
        self.input_dir = Path(input_dir)
        self.output_file = output_file
        
    def determine_sitemap_type(self, xml_files):
        """Determina se devemos criar um sitemapindex ou urlset baseado nos arquivos"""
        sitemapindex_count = 0
        urlset_count = 0
        
        for xml_file in xml_files:
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                
                # Remove namespace para comparação
                tag_name = root.tag
                if '}' in tag_name:
                    tag_name = tag_name.split('}')[1]
                
                if tag_name == 'sitemapindex':
                    sitemapindex_count += 1
                elif tag_name == 'urlset':
                    urlset_count += 1
                    
            except ET.ParseError:
                continue
        
        # Se temos sitemapindex, priorizamos criar um sitemapindex
        if sitemapindex_count > 0:
            return 'sitemapindex'
        else:
            return 'urlset'
    
    def find_xml_files(self):
        """Encontra todos os arquivos XML na pasta de entrada"""
        xml_files = list(self.input_dir.glob("*.xml"))
        logger.info(f"Encontrados {len(xml_files)} arquivos XML em {self.input_dir}")
        return xml_files
    
    def parse_xml_file(self, file_path):
        """Parse de um arquivo XML individual"""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            logger.info(f"Arquivo processado com sucesso: {file_path.name}")
            return root
        except ET.ParseError as e:
            logger.error(f"Erro ao fazer parse do arquivo {file_path.name}: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado ao processar {file_path.name}: {e}")
            return None
        """Parse de um arquivo XML individual"""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            logger.info(f"Arquivo processado com sucesso: {file_path.name}")
            return root
        except ET.ParseError as e:
            logger.error(f"Erro ao fazer parse do arquivo {file_path.name}: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado ao processar {file_path.name}: {e}")
            return None
    
    def create_unified_root(self, first_root):
        """Cria o elemento raiz para o XML unificado baseado no primeiro arquivo"""
        # Remove prefixos de namespace para criar tags limpas
        tag_name = first_root.tag
        if '}' in tag_name:
            tag_name = tag_name.split('}')[1]
        
        # Para sitemaps, sempre usa o namespace padrão
        if tag_name in ['sitemapindex', 'urlset']:
            namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
            unified_root = ET.Element(tag_name)
            unified_root.set('xmlns', namespace)
            
            # Adiciona namespace de imagens se presente no original
            for key, value in first_root.attrib.items():
                if 'image' in value:
                    unified_root.set('xmlns:image', value)
        else:
            # Para outros tipos de XML, mantém o comportamento original
            unified_root = ET.Element(first_root.tag, first_root.attrib)
            
            # Copia namespaces se existirem
            for key, value in first_root.attrib.items():
                if key.startswith('xmlns'):
                    unified_root.set(key, value)
                
        return unified_root
    
    def clean_element(self, element):
        """Remove prefixos de namespace dos elementos para sitemap limpo"""
        # Remove prefixo do namespace da tag
        if '}' in element.tag:
            element.tag = element.tag.split('}')[1]
        
        # Limpa recursivamente todos os elementos filhos
        for child in element:
            self.clean_element(child)
        
        return element
    
    def merge_elements(self, unified_root, xml_root):
        """Merge dos elementos de um XML para o XML unificado"""
        # Se o XML tem filhos diretos, adiciona todos eles
        for child in xml_root:
            # Limpa o elemento antes de adicionar
            clean_child = self.clean_element(child)
            unified_root.append(clean_child)
    
    def prettify_xml(self, element):
        """Formata o XML para ficar mais legível"""
        # Converte para string primeiro
        rough_string = ET.tostring(element, encoding='utf-8')
        
        # Parse novamente para formatação
        reparsed = minidom.parseString(rough_string)
        
        # Gera XML formatado sem declaração XML extra
        pretty_xml = reparsed.toprettyxml(indent="  ", encoding='utf-8')
        
        # Remove linhas em branco extras
        lines = pretty_xml.decode('utf-8').split('\n')
        clean_lines = [line for line in lines if line.strip()]
        
        return '\n'.join(clean_lines).encode('utf-8')
    
    def unify_xml_files(self):
        """Função principal para unificar os arquivos XML"""
        xml_files = self.find_xml_files()
        
        if not xml_files:
            logger.warning("Nenhum arquivo XML encontrado para processar")
            return False
        
        # Determina o tipo de sitemap a ser criado
        target_type = self.determine_sitemap_type(xml_files)
        logger.info(f"Tipo de sitemap detectado: {target_type}")
        
        # Cria o elemento raiz baseado no tipo detectado
        namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
        unified_root = ET.Element(target_type)
        unified_root.set('xmlns', namespace)
        
        # Processa todos os arquivos
        for xml_file in xml_files:
            root = self.parse_xml_file(xml_file)
            if root is not None:
                # Remove namespace para comparação
                tag_name = root.tag
                if '}' in tag_name:
                    tag_name = tag_name.split('}')[1]
                
                # Se estamos criando sitemapindex, só inclui elementos de sitemapindex
                if target_type == 'sitemapindex' and tag_name == 'sitemapindex':
                    self.merge_elements(unified_root, root)
                # Se estamos criando urlset, só inclui elementos de urlset
                elif target_type == 'urlset' and tag_name == 'urlset':
                    self.merge_elements(unified_root, root)
                else:
                    logger.warning(f"Arquivo {xml_file.name} tem tipo incompatível ({tag_name}) com destino ({target_type})")
        
        # Salva o arquivo unificado
        try:
            # Cria pasta output se não existir
            output_path = Path(self.output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            pretty_xml = self.prettify_xml(unified_root)
            with open(self.output_file, 'wb') as f:
                f.write(pretty_xml)
            
            logger.info(f"Arquivo unificado salvo como: {self.output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao salvar o arquivo unificado: {e}")
            return False

def main():
    """Função principal"""
    logger.info("Iniciando XML Unifier...")
    
    # Verifica se a pasta files existe
    files_dir = Path("files")
    if not files_dir.exists():
        logger.error("Pasta 'files' não encontrada!")
        logger.info("Criando pasta 'files'...")
        files_dir.mkdir()
        logger.warning("Pasta 'files' criada. Adicione os arquivos XML e execute novamente.")
        return
    
    # Cria o unificador e executa
    unifier = XMLUnifier()
    success = unifier.unify_xml_files()
    
    if success:
        logger.info("Unificação concluída com sucesso!")
    else:
        logger.error("Falha na unificação dos arquivos XML")

if __name__ == "__main__":
    main()
